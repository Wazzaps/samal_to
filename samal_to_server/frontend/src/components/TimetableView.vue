<template>
  <div>
    <!-- <center>
      <b-button variant="outline-secondary" v-b-modal.timerange-picker>
        <b>2021-05-22</b> 10:00 – <b>2021-05-22</b> 13:00
      </b-button>
    </center> -->

    <canvas id="timetable_header"/>
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
      this.renderTimetableHeader();
      this.renderTimetableContents();

    },
    renderTimetableHeader() {
      const canvas = document.getElementById('timetable_header');
      const ctx = canvas.getContext('2d');

      const tasks = Object.values(this.$store.state.tasks);

      // Calculate height of vertical task name stack
      const canvasWidth = canvas.clientWidth;
      const labelVMargin = 3;
      const labelHPadding = 3;
      let timeBarWidth = 64;
      const taskWidth = parseInt((canvasWidth - timeBarWidth) / tasks.length);
      timeBarWidth = canvasWidth - taskWidth * tasks.length;

      ctx.font = '12px sans';
      const taskNameLengths = tasks.map(t => ctx.measureText(t.name).width);

      let taskStackHeight = 7;
      for (let stackHeight = 1; stackHeight <= 7; stackHeight++) {
        let works = true;
        // console.log(`trying stack of ${stackHeight}`);
        for (let i = stackHeight; i < taskNameLengths.length; i++) {
          if (taskNameLengths[i] + 2 * labelHPadding > stackHeight * taskWidth) {
            works = false;
            break;
          }
        }
        if (works) {
          taskStackHeight = stackHeight;
          break;
        }
      }

      // Various constants
      const pillarWidth = 4;
      const labelOffset = 3;
      const labelTextOffset = 16;
      const bottomPadding = 4;
      const heightPerLabel = 23;
      const headerHeight = heightPerLabel * taskStackHeight + bottomPadding;

      canvas.width = canvasWidth;
      canvas.height = headerHeight;

      // Draw task label BGs
      tasks.forEach((task, i) => {
        const heightIdx = taskStackHeight - (i % taskStackHeight) - 1;
        // Pillar Shadow
        ctx.fillStyle = `rgb(80, 80, 80)`;
        const pillarX = parseInt(timeBarWidth + (i + 0.5) * taskWidth - pillarWidth / 2);
        ctx.fillRect(
          pillarX - 1,
          heightPerLabel * heightIdx + labelVMargin + heightPerLabel - 2 * labelVMargin,
          pillarWidth + 2,
          headerHeight
        );

        // Label BG Shadow
        const labelX = parseInt(timeBarWidth + (i + 1) * taskWidth - 2 * labelHPadding - taskNameLengths[i]);
        const labelWidth = parseInt(taskNameLengths[i] + 2 * labelHPadding);
        ctx.fillRect(
          labelX - 1,
          heightPerLabel * heightIdx + labelVMargin - 1,
          labelWidth + 2,
          heightPerLabel - 2 * labelVMargin + 2
        );

        // Pillar
        ctx.fillStyle = `#eeeeee`;
        ctx.fillRect(
          pillarX,
          heightPerLabel * heightIdx + labelVMargin + heightPerLabel - 2 * labelVMargin,
          pillarWidth,
          headerHeight
        );

        // Label BG
        ctx.fillRect(
          labelX,
          heightPerLabel * heightIdx + labelVMargin,
          labelWidth,
          heightPerLabel - 2 * labelVMargin
        );
      });

      // Draw task labels
      ctx.fillStyle = 'rgb(0, 0, 0)';
      ctx.textAlign = "end";
      ctx.font = '12px sans';
      tasks.forEach((task, i) => {
        const heightIdx = taskStackHeight - (i % taskStackHeight) - 1;
        ctx.fillText(
          task.name,
          timeBarWidth + (i + 1) * taskWidth - labelHPadding,
          labelTextOffset + heightPerLabel * heightIdx
        );
      });

      // ctx.fillStyle = 'rgb(0, 0, 0)';
      // ctx.fillRect(timeBarWidth, 0, canvasWidth - timeBarWidth, headerHeight);
    },
    renderTimetableContents() {
      const canvas = document.getElementById('timetable_contents');
      const ctx = canvas.getContext('2d');

      const tasks = Object.values(this.$store.state.tasks);

      const timeStart = new Date('2020-12-17T12:00:00').getTime();
      const timeEnd = new Date('2020-12-18T12:00:00').getTime();
      const timeHours = (timeEnd - timeStart) / 1000 / 60 / 60;

      // Various constants
      const timebarHourHeight = 56;
      const timebar30mHeight = parseInt(timebarHourHeight / 2);
      const timebar15mHeight = parseInt(timebarHourHeight / 4);
      const timebarFirstOffset = 15;
      const timebarOffset = 32;
      const timebarTextPadding = 3;
      const bottomPadding = 10;

      const canvasHeight = timebarOffset + timebarTextPadding + timebarHourHeight * timeHours + bottomPadding;
      const canvasWidth = canvas.clientWidth;
      let timeBarWidth = 64;
      const taskWidth = parseInt((canvasWidth - timeBarWidth) / tasks.length);
      timeBarWidth = canvasWidth - taskWidth * tasks.length;
      const pillarWidth = 4;
      const bubblePadding = 2;
      const bubbleBorder = 3;

      canvas.width = canvasWidth;
      canvas.height = canvasHeight;
      ctx.textBaseline = "alphabetic";

      // -- Draw timebar --
      // ctx.fillStyle = 'rgb(240, 256, 240)';
      ctx.fillStyle = 'rgb(256, 256, 256)';
      ctx.fillRect(0, 0, timeBarWidth, canvasHeight);

      // Draw timebar lines
      ctx.strokeStyle = 'rgb(0, 0, 0)';
      ctx.lineWidth = 1;
      for (let i = 0; i < timeHours + 1; i++) {
        ctx.beginPath();
        ctx.setLineDash([]);
        ctx.moveTo(
          0,
          0.5 + timebarOffset + timebarTextPadding + i * timebarHourHeight
        );
        ctx.lineTo(
          canvasWidth,
          0.5 + timebarOffset + timebarTextPadding + i * timebarHourHeight
        );
        ctx.stroke();
      }
      ctx.strokeStyle = 'rgb(200, 200, 200)';
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
      ctx.strokeStyle = 'rgb(200, 200, 200)';
      ctx.setLineDash([3, 7]);
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
      ctx.font = '10px sans';
      let curDate = new Date(timeStart).toLocaleString('sv', {timeZoneName: 'short'}).split(" ")[0];
      ctx.fillText(curDate, timeBarWidth - 3, timebarFirstOffset);

      // Draw time labels
      for (let i = 0; i < timeHours + 1; i++) {
        const nextDate = new Date(timeStart + i * 1000 * 60 * 60);
        const nextDateFormatted = nextDate.toLocaleString('sv', {timeZoneName: 'short'}).split(" ")[0];
        if (nextDateFormatted != curDate) {
          ctx.font = '10px sans';
          ctx.fillText(nextDateFormatted, timeBarWidth - 3, timebarOffset + i * timebarHourHeight);
        } else {
          ctx.font = '12px sans';
          ctx.fillText(
            `${zpad(nextDate.getHours())}:${zpad(nextDate.getMinutes())}`,
            timeBarWidth - 3, timebarOffset + i * timebarHourHeight
          );
        }
        curDate = nextDateFormatted;
      }

      // Draw task pillars
      for (let i = 0; i < tasks.length; i++) {
        const pillarX = parseInt(timeBarWidth + (i + 0.5) * taskWidth - pillarWidth / 2);
        ctx.fillStyle = `rgb(80, 80, 80)`;

        // Pillar shadow
        ctx.fillRect(
          pillarX - 1,
          0,
          pillarWidth + 2,
          canvasHeight
        );

        // Pillar
        ctx.fillStyle = `#eeeeee`;
        ctx.fillRect(
          pillarX,
          0,
          pillarWidth,
          canvasHeight
        );
      }

      // Draw task bubbles
      for (let i = 0; i < tasks.length; i++) {
        for (const assignment of Object.values(tasks[i].shifts)) {
          const bubbleX = parseInt(timeBarWidth + i * taskWidth + bubblePadding);
          const bubbleY = parseInt(timebarOffset + timebarTextPadding + (assignment.start - 12) * timebarHourHeight);
          const bubbleW = parseInt(taskWidth - 2 * bubblePadding);
          const bubbleH = parseInt(assignment.duration * timebarHourHeight);

          // Bubble base
          ctx.fillStyle = assignment.assigned ? '#C20E20' : '#777';
          ctx.shadowColor = assignment.assigned ? '#AA0C1CEE' : '#111';
          ctx.shadowBlur = 4;
          ctx.shadowOffsetY = 2;
          ctx.fillRect(
            bubbleX,
            bubbleY,
            bubbleW,
            bubbleH
          );
          ctx.shadowColor = 'transparent';

          // Bubble bottom border
          ctx.fillStyle = assignment.assigned ? '#7c0b17' : '#444';
          ctx.fillRect(
            bubbleX,
            bubbleY + bubbleH - bubbleBorder,
            bubbleW,
            bubbleBorder
          );
          ctx.shadowColor = 'transparent';

          // Assigned ID
          ctx.font = "bold 18px rubik";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillStyle = '#fff';
          ctx.shadowColor = '#222';
          ctx.shadowBlur = 4;
          ctx.shadowOffsetY = 1;
          ctx.fillText(assignment.assigned || "-", bubbleX + bubbleW / 2, bubbleY + bubbleH / 2);
          ctx.shadowColor = 'transparent';
          ctx.shadowOffsetY = 0;
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

</style>
