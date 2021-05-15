<template>
  <div>
    <b-button
      @click="shareToPng"
      class="mb-3 ml-2 float-right"
      variant="outline-primary"
    >Share PNG</b-button>
    <b-button
      @click="shareToJson"
      class="mb-3 ml-2 float-right"
      variant="outline-primary"
    >Share Link</b-button>
    <b-button
      @click="autoSolve"
      :disabled="autoSolveDisabled"
      class="mb-3 float-right"
      variant="primary"
    >Auto Assign</b-button>

    <canvas id="timetable_contents"/>
  </div>
</template>

<script>
export default {
  data: () => ({
    autoSolveDisabled: false,
  }),
  methods: {
    renderTimetable() {
      const tasks = Object.entries(this.$store.state.tasks);
      let tracks = [];
      let minTime = Infinity;
      let maxTime = 0;

      tasks.forEach(([taskId, task]) => {
        Object.values(task.shifts).forEach(shift => {
          if (shift.start < minTime) {
            minTime = shift.start;
          }
          if (shift.start + shift.duration > maxTime) {
            maxTime = shift.start + shift.duration;
          }

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
      });

      if (minTime == Infinity || maxTime == 0) {
        minTime = maxTime = new Date().getTime() / 1000;
      }

      this.renderTimetableContents(tracks, minTime * 1000, maxTime * 1000);
    },
    renderTimetableContents(tracks, timeStart, timeEnd) {
      const canvas = document.getElementById('timetable_contents');
      const ctx = canvas.getContext('2d');

      const people = this.$store.state.people;
      const tasks = this.$store.state.tasks;

      const timeHours = (timeEnd - timeStart) / 1000 / 60 / 60;

      // Various constants
      const pixelMult = devicePixelRatio;
      const timebarHourHeight = 60 * pixelMult;
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

      // -- Draw bg --
      ctx.fillStyle = 'rgb(256, 256, 256)';
      ctx.fillRect(0, 0, canvasWidth, canvasHeight);

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
      const bubbleColors = ["#C20E20", "#FFBAA4", "#006ECB", "#FFDBF0", "#00675E", "#68E7E5"];
      const bubbleTextColors = ["#fff", "#000", "#fff", "#000", "#fff", "#000"];
      const bubbleTextShadowColors = ["#222", "#ffffff44", "#222", "#ffffff44", "#222", "#ffffff44"];
      const bubbleShadowColors = ["#AA0C1CEE", "#c57e68EE", "#006CC7EE", "#c7afb3EE", "#00675EEE", "#59b6b4EE"];
      for (let i = 0; i < tracks.length; i++) {
        for (const [taskId, shift] of tracks[i]) {
          const bubbleX = parseInt(timeBarWidth + i * trackWidth + bubblePadding);
          const bubbleY = parseInt(timebarOffset + timebarTextPadding + (shift.start - timeStart / 1000) / (60 * 60) * timebarHourHeight);
          const bubbleW = parseInt(trackWidth - 2 * bubblePadding);
          const bubbleH = parseInt(shift.duration / (60 * 60) * timebarHourHeight);

          // Bubble base
          ctx.fillStyle = shift.assigned ? bubbleColors[people[shift.assigned].ident_color] : '#777';
          ctx.shadowColor = shift.assigned ? bubbleShadowColors[people[shift.assigned].ident_color] : '#111';
          ctx.shadowBlur = 6 * pixelMult;
          ctx.shadowOffsetY = 2 * pixelMult;
          ctx.fillRect(
            bubbleX,
            bubbleY,
            bubbleW,
            bubbleH
          );
          ctx.shadowColor = 'transparent';

          // Bubble bottom border
          ctx.fillStyle = shift.assigned ? '#00000066' : '#444';
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
          ctx.fillStyle = shift.assigned ? bubbleTextColors[people[shift.assigned].ident_color] : '#fff';
          ctx.shadowColor = shift.assigned ? bubbleTextShadowColors[people[shift.assigned].ident_color] : '#222';
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
            assignedPerson = people[assignedPerson].num;
          } else {
            assignedPerson = "?";
          }
          ctx.font = `bold ${numFontSize}px rubik, sans`;
          ctx.shadowOffsetY = 1 * pixelMult;
          ctx.fillText(assignedPerson, bubbleX + bubbleW / 2, bubbleY + numFontSize);
          ctx.shadowColor = 'transparent';
          ctx.shadowOffsetY = 0;
          ctx.shadowOffsetX = 0;
        }
      }
    },
    createSolveRequest() {
      // Calculate task time range
      let minTime = Infinity;
      let maxTime = 0;

      Object.entries(this.$store.state.tasks).forEach(([_taskId, task]) => {
        Object.values(task.shifts).forEach(shift => {
          if (shift.start < minTime) {
            minTime = shift.start;
          }
          if (shift.start + shift.duration > maxTime) {
            maxTime = shift.start + shift.duration;
          }
        });
      });

      if (minTime == Infinity || maxTime == 0) {
        minTime = maxTime = new Date().getTime() / 1000;
      }

      // Create request
      let req = {
        people: [],
        shifts: [],
        settings: {
          min_rest_per_day: 360,
          longsleep_min_rest_per_day: 480,
          overtime_interval_min: 15,
          overtime_threshold: 12,
          max_overtime_intervals: 8,
          longsleep_max_overtime_intervals: 12,
          suffer_per_overtime_min: 5,
          longsleep_suffer_per_overtime_min: 0,
          timeout: 3
        }
      };

      Object.values(this.$store.state.tasks).forEach(task => {
        Object.values(task.shifts).forEach(shift => {
          req.shifts.push({
            time: parseInt((shift.start - minTime) / 60),
            duration: parseInt(shift.duration / 60),
            cost: 100,
            task
          });
        });
      });

      Object.values(this.$store.state.people).forEach(person => {
        const personObj = {
            restricted_tasks: [],
            assigned_tasks: [],
            prefers_longer_sleep: false
        };
        req.shifts.forEach((shift, shift_idx) => {
          for (const tag of shift.task.mustNotHaveTags) {
            if (person.tags.includes(tag)) {
              personObj.restricted_tasks.push(shift_idx);
              return;
            }
          }
          for (const tag of shift.task.mustHaveTags) {
            if (!person.tags.includes(tag)) {
              personObj.restricted_tasks.push(shift_idx);
              return;
            }
          }
        });
        req.people.push(personObj);
      });

      req.shifts.forEach(shift => {
        shift.task = undefined;
      });

      return req;
    },
    applySolution(solution) {
      let shifts = Object.entries(this.$store.state.tasks).flatMap(([taskId, task]) => {
        return Object.keys(task.shifts).map(shiftId => {
          return [taskId, shiftId];
        });
      });

      let people = Object.keys(this.$store.state.people);
      let assignments = [];
      solution.forEach((personIdx, shiftIdx) => {
        assignments.push([...shifts[shiftIdx], people[personIdx]]);
      });

      this.$store.commit('assignMultipleShifts', assignments);
      this.renderTimetable();
    },
    async autoSolve() {
      let req = this.createSolveRequest();

      this.autoSolveDisabled = true;

      let res = await fetch("https://jn3b6iu9s3.execute-api.eu-central-1.amazonaws.com/default/samal_to", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(req)
      });
      res = await res.json();

      this.autoSolveDisabled = false;

      if (res.solution_type != "Infeasible") {
        this.applySolution(res.shifts);
      }
    },
    shiftMinStartDate() {
      let minStartTime = Infinity;
      for (const task of Object.values(this.$store.state.tasks)) {
        for (const shift of Object.values(task.shifts)) {
          if (shift.start < minStartTime) {
            minStartTime = shift.start;
          }
        }
      }

      return new Date(minStartTime * 1000).toLocaleString('sv', {timeZoneName: 'short'}).split(" ")[0];
    },
    shareToPng() {
      const canvas = document.getElementById('timetable_contents');
      const title = `Timetable for ${this.shiftMinStartDate()}`;
      canvas.toBlob((blob) => {
        let file = new File([blob], "timetable.jpg", {type: 'image/png'});
        let filesArray = [file];
        const sharePayload = {
          title: title,
          files: filesArray
        };
        if (navigator.canShare && navigator.canShare(sharePayload)) {
          navigator.share(sharePayload);
        } else {
          open().document.write('<title>' + title + '</title><img src="' + canvas.toDataURL() + '"/>');
        }
      });
    },
    shareToJson() {
      const s = window.LZUTF8.compress(JSON.stringify(this.$store.state), {outputEncoding: "Base64"});
      console.log(s);
    },
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
