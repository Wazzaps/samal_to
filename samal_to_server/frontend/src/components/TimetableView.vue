<template>
  <div>
    <!-- <center>
      <b-button variant="outline-secondary" v-b-modal.timerange-picker>
        <b>2021-05-22</b> 10:00 – <b>2021-05-22</b> 13:00
      </b-button>
    </center> -->

    <canvas id="timetable_contents"/>

    <b-modal id="timerange-picker" title="Select date &amp; time range">
      <h5>Start date:</h5>
      <b-row>
        <b-col class="pr-1"><b-datepicker/></b-col>
        <b-col class="pl-1"><b-timepicker/></b-col>
      </b-row>
      <h5 class="mt-4">End date:</h5>
      <b-row>
        <b-col class="pr-1"><b-datepicker/></b-col>
        <b-col class="pl-1"><b-timepicker/></b-col>
      </b-row>
      <template #modal-footer="{ ok }">
        <b-button variant="primary" @click="ok()">
          Save
        </b-button>
      </template>
    </b-modal>
  </div>
</template>

<script>
export default {
  methods: {
    increment () {
      this.$store.commit('increment')
    },
    renderTimetable() {
      const tasks = Object.entries(this.$store.state.tasks);
      let tracks = [];
      tasks.forEach(([taskId, task]) => {
        Object.values(task.shifts).forEach(shift => {
          function trackIsAvailable(track, start, duration) {
            return track.every(([_, trackShift]) => {
              // No overlapping shifts in this track
              return !((shift.start + shift.duration) > trackShift.start && (trackShift.start + trackShift.duration) > shift.start)
            });
          }
          for (const track of tracks) {
            if (trackIsAvailable(track, shift.start, shift.duration)) {
              track.push([taskId, shift]);
              return;
            }
          }
          tracks.push([[taskId, shift]]);
        });
      });

      // Sort shifts in track by start time, to prevent inconsistent shadow overlap
      tracks.forEach(track => {
        track.sort(([_1, shiftA], [_2, shiftB]) => {
          return shiftA.start > shiftB.start ? 1 : -1;
        });
      })

      this.renderTimetableContents(tracks);
    },
    renderTimetableContents(tracks) {
      const canvas = document.getElementById('timetable_contents');
      const ctx = canvas.getContext('2d');

      const tasks = this.$store.state.tasks;

      const timeStart = new Date('2020-12-17T12:00:00').getTime();
      const timeEnd = new Date('2020-12-18T12:00:00').getTime();
      const timeHours = (timeEnd - timeStart) / 1000 / 60 / 60;

      // Various constants
      const pixelMult = devicePixelRatio;
      const timebarHourHeight = 56 * pixelMult;
      const timebar30mHeight = parseInt(timebarHourHeight / 2);
      const timebar15mHeight = parseInt(timebarHourHeight / 4);
      const timebarFirstOffset = 15 * pixelMult;
      const timebarOffset = 32 * pixelMult;
      const timebarTextPadding = 3 * pixelMult;
      const bottomPadding = 10 * pixelMult;

      const canvasHeight = timebarOffset + timebarTextPadding + timebarHourHeight * timeHours + bottomPadding;
      const canvasWidth = canvas.clientWidth * pixelMult;
      let timeBarWidth = 64 * pixelMult;
      const trackWidth = parseInt((canvasWidth - timeBarWidth) / tracks.length);
      timeBarWidth = canvasWidth - trackWidth * tracks.length;
      const pillarWidth = 4 * pixelMult;
      const bubblePadding = 4 * pixelMult;
      const bubbleBorder = 3 * pixelMult;

      canvas.width = canvasWidth;
      canvas.height = canvasHeight;
      ctx.textBaseline = "alphabetic";

      // -- Draw timebar --
      // ctx.fillStyle = 'rgb(240, 256, 240)';
      ctx.fillStyle = 'rgb(256, 256, 256)';
      ctx.fillRect(0, 0, timeBarWidth, canvasHeight);

      // Draw timebar lines
      ctx.strokeStyle = 'rgb(60, 60, 60)';
      ctx.lineWidth = 2 * pixelMult;
      for (let i = 0; i < timeHours + 1; i++) {
        ctx.beginPath();
        ctx.setLineDash([]);
        ctx.moveTo(
          0,
          timebarOffset + timebarTextPadding + i * timebarHourHeight
        );
        ctx.lineTo(
          canvasWidth,
          timebarOffset + timebarTextPadding + i * timebarHourHeight
        );
        ctx.stroke();
      }
      ctx.lineWidth = 1 * pixelMult;
      ctx.strokeStyle = 'rgb(120, 120, 120)';
      for (let i = 0; i < timeHours; i++) {
        ctx.beginPath();
        ctx.setLineDash([]);
        ctx.moveTo(
          0,
          0.5 + timebarOffset + timebar30mHeight + timebarTextPadding + i * timebarHourHeight
        );
        ctx.lineTo(
          canvasWidth,
          0.5 + timebarOffset + timebar30mHeight + timebarTextPadding + i * timebarHourHeight
        );
        ctx.stroke();
      }
      ctx.strokeStyle = 'rgb(120, 120, 120)';
      ctx.setLineDash([3 * pixelMult, 7 * pixelMult]);
      for (let i = 0; i < timeHours; i++) {
        ctx.beginPath();
        ctx.moveTo(
          0,
          0.5 + timebarOffset + timebar15mHeight + timebarTextPadding + i * timebarHourHeight
        );
        ctx.lineTo(
          canvasWidth,
          0.5 + timebarOffset + timebar15mHeight + timebarTextPadding + i * timebarHourHeight
        );
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(
          0,
          0.5 + timebarOffset + timebar30mHeight + timebar15mHeight + timebarTextPadding + i * timebarHourHeight
        );
        ctx.lineTo(
          canvasWidth,
          0.5 + timebarOffset + timebar30mHeight + timebar15mHeight + timebarTextPadding + i * timebarHourHeight
        );
        ctx.stroke();
      }

      // -- Draw timebar labels --
      function zpad(num) {
        return num.toString().padStart(2, "0");
      }

      // Draw first date
      ctx.fillStyle = 'rgb(0, 0, 0)';
      ctx.textAlign = "end";
      ctx.font = `${10 * pixelMult}px sans`;
      let curDate = new Date(timeStart).toLocaleString('sv', {timeZoneName: 'short'}).split(" ")[0];
      ctx.fillText(curDate, timeBarWidth - 3, timebarFirstOffset);

      // Draw time labels
      for (let i = 0; i < timeHours + 1; i++) {
        const nextDate = new Date(timeStart + i * 1000 * 60 * 60);
        const nextDateFormatted = nextDate.toLocaleString('sv', {timeZoneName: 'short'}).split(" ")[0];
        if (nextDateFormatted != curDate) {
          ctx.font = `${10 * pixelMult}px sans`;
          ctx.fillText(nextDateFormatted, timeBarWidth - 3, timebarOffset + i * timebarHourHeight);
        } else {
          ctx.font = `${12 * pixelMult}px sans`;
          ctx.fillText(
            `${zpad(nextDate.getHours())}:${zpad(nextDate.getMinutes())}`,
            timeBarWidth - 3, timebarOffset + i * timebarHourHeight
          );
        }
        curDate = nextDateFormatted;
      }

      // Draw task pillars
      // for (let i = 0; i < tracks.length; i++) {
      //   const pillarX = parseInt(timeBarWidth + (i + 0.5) * trackWidth - pillarWidth / 2);
      //   ctx.fillStyle = `rgb(80, 80, 80)`;

      //   // Pillar shadow
      //   ctx.fillRect(
      //     pillarX - pixelMult,
      //     0,
      //     pillarWidth + 2 * pixelMult,
      //     canvasHeight
      //   );

      //   // Pillar
      //   ctx.fillStyle = `#eeeeee`;
      //   ctx.fillRect(
      //     pillarX,
      //     0,
      //     pillarWidth,
      //     canvasHeight
      //   );
      // }

      // Draw task bubbles
      for (let i = 0; i < tracks.length; i++) {
        for (const [taskId, shift] of tracks[i]) {
          const bubbleX = parseInt(timeBarWidth + i * trackWidth + bubblePadding);
          const bubbleY = parseInt(timebarOffset + timebarTextPadding + (shift.start - 12) * timebarHourHeight);
          const bubbleW = parseInt(trackWidth - 2 * bubblePadding);
          const bubbleH = parseInt(shift.duration * timebarHourHeight);

          // Bubble base
          ctx.fillStyle = shift.assigned ? '#C20E20' : '#777';
          ctx.shadowColor = shift.assigned ? '#AA0C1CEE' : '#111';
          ctx.shadowBlur = 4 * pixelMult;
          ctx.shadowOffsetY = 2 * pixelMult;
          ctx.fillRect(
            bubbleX,
            bubbleY,
            bubbleW,
            bubbleH
          );
          ctx.shadowColor = 'transparent';

          // Bubble bottom border
          ctx.fillStyle = shift.assigned ? '#7c0b17' : '#444';
          ctx.fillRect(
            bubbleX,
            bubbleY + bubbleH - bubbleBorder,
            bubbleW,
            bubbleBorder
          );
          ctx.shadowColor = 'transparent';

          // Task label
          const numFontSize = 18 * pixelMult;
          let taskNameFontSize = 14;
          for (; taskNameFontSize > 8; taskNameFontSize--) {
            ctx.font = `${taskNameFontSize * pixelMult}px rubik, sans`;
            if (ctx.measureText(tasks[taskId].name).width <= bubbleH - numFontSize) {
              break;
            }
          }
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillStyle = '#fff';
          ctx.shadowColor = '#222';
          ctx.shadowBlur = 4 * pixelMult;
          const textX = bubbleX + bubbleW / 2;
          const textY = bubbleY + bubbleH / 2;
          ctx.save();
          ctx.translate(textX, textY);
          ctx.rotate(-Math.PI/2);
          ctx.fillText(tasks[taskId].name, 0, 0);
          ctx.restore();

          // Assigned ID
          let assignedPerson = shift.assigned;
          if (assignedPerson) {
            assignedPerson = this.$store.state.people[assignedPerson].num;
          } else {
            assignedPerson = "-";
          }
          ctx.font = `bold ${numFontSize}px rubik, sans`;
          ctx.shadowOffsetY = 1 * pixelMult;
          ctx.fillText(assignedPerson, bubbleX + bubbleW / 2, bubbleY + numFontSize);
          ctx.shadowColor = 'transparent';
          ctx.shadowOffsetY = 0;
          ctx.shadowOffsetX = 0;
        }
      }
    }
  },
  mounted() {
    this.renderTimetable();
    setTimeout(() => this.renderTimetable(), 300);
  }
}
</script>

<style scoped>
#timetable_contents, #timetable_header {
  width: 100%;
  display: block;
}

#timetable_header {
  position: sticky;
  top: 10px;
  background: #fff;
  box-shadow: 0 -200px 0 200px #fff;
  z-index: -10;
}

#timetable_contents {
  position: relative;
  z-index: -11;
  background: #fff;
}

</style>
