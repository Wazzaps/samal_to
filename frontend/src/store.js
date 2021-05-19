import Vuex from 'vuex'

const baseTime = 1620248400; // Posix time for: Thu May 06 2021 00:00:00 GMT+0300 (Israel Daylight Time)
const timeMult = 60 * 60; // Hours -> Seconds

const store = new Vuex.Store({
  state: {
    tags: {},
    people: {},
    tasks: {},
  },
  mutations: {
    addPerson(state, [personId, personNum]) {
      state.people[personId] = {
        num: personNum,
        name: "",
        phoneNum: "",
        tags: [],
        ident_color: personId % 6,
        // ident_pattern: pattern,
      };
    },

    addTask(state, taskId) {
      state.tasks[taskId] = {
        name: "",
        description: "",
        difficulty: 3,
        mustHaveTags: [],
        mustNotHaveTags: [],
        shifts: {},
      };
    },

    duplicateTask(state, [newTaskId, srcTaskId]) {
      state.tasks[newTaskId] = JSON.parse(JSON.stringify(state.tasks[srcTaskId]));
      state.tasks[newTaskId].name += " (copy)";
      for (const shift of Object.values(state.tasks[newTaskId].shifts)) {
        shift.assigned = null;
      }
    },

    deletePerson(state, personId) {
      for (const task of Object.values(state.tasks)) {
        for (const shift of Object.values(task.shifts)) {
          if (shift.assigned == personId) {
            shift.assigned = null;
          }
        }
      }
      delete state.people[personId];
    },

    duplicatePerson(state, [newPersonId, srcPersonId]) {
      state.people[newPersonId] = JSON.parse(JSON.stringify(state.people[srcPersonId]));
      state.people[newPersonId].name += " (copy)";
      state.people[newPersonId].ident_color = newPersonId % 6;
    },

    deleteTask(state, taskId) {
      delete state.tasks[taskId];
    },

    personAddTag(state, [personId, tagId]) {
      state.people[personId].tags.push(tagId);
    },

    personRemoveTag(state, [personId, tagId]) {
      state.people[personId].tags.splice(
        state.people[personId].tags.indexOf(tagId),
        1
      );
    },

    taskAssignShift(state, [taskId, shiftId, personId]) {
      state.tasks[taskId].shifts[shiftId].assigned = personId;
    },

    unassignAllShifts(state) {
      for (const task of Object.values(state.tasks)) {
        for (const shift of Object.values(task.shifts)) {
          shift.assigned = null;
        }
      }
    },

    taskAddRequiredTag(state, [taskId, tagId]) {
      state.tasks[taskId].mustHaveTags.push(tagId);
    },

    taskRemoveRequiredTag(state, [taskId, tagId]) {
      state.tasks[taskId].mustHaveTags.splice(
        state.tasks[taskId].mustHaveTags.indexOf(tagId),
        1
      );
    },

    taskAddDisqualifyingTag(state, [taskId, tagId]) {
      state.tasks[taskId].mustNotHaveTags.push(tagId);
    },

    taskRemoveDisqualifyingTag(state, [taskId, tagId]) {
      state.tasks[taskId].mustNotHaveTags.splice(
        state.tasks[taskId].mustNotHaveTags.indexOf(tagId),
        1
      );
    },

    taskAddShift(state, [taskId, shiftId]) {
      let currentDate = new Date();
      currentDate.setMinutes(0, 0, 0);
      state.tasks[taskId].shifts[shiftId] = {
        start: currentDate.getTime() / 1000,
        duration: 60 * 60, // 1 Hour
        assigned: null
      };
    },

    taskDeleteShift(state, [taskId, shiftId]) {
      delete state.tasks[taskId].shifts[shiftId];
    },

    shiftSetTime(state, [taskId, shiftId, timeRange]) {
      state.tasks[taskId].shifts[shiftId].start = parseInt(timeRange.start.getTime() / 1000);
      state.tasks[taskId].shifts[shiftId].duration = parseInt(
        (timeRange.end.getTime() - timeRange.start.getTime()) / 1000
      );
    },

    personUpdatePhoneNum(state, [personId, phoneNum]) {
      state.people[personId].phoneNum = phoneNum;
    },

    personUpdateName(state, [personId, name]) {
      state.people[personId].name = name;
    },

    taskUpdateName(state, [taskId, name]) {
      state.tasks[taskId].name = name;
    },

    taskUpdateDescription(state, [taskId, description]) {
      state.tasks[taskId].description = description;
    },

    taskUpdateDifficulty(state, [taskId, difficulty]) {
      state.tasks[taskId].difficulty = difficulty;
    },

    createTag(state, [tagId, tagName]) {
      state.tags[tagId] = tagName;
    },

    assignMultipleShifts(state, assignments) {
      assignments.forEach(([taskId, shiftId, personId]) => {
        state.tasks[taskId].shifts[shiftId].assigned = personId;
      })
    },

    rebaseShifts(state, delta) {
      for (const task of Object.values(state.tasks)) {
        for (const shift of Object.values(task.shifts)) {
          shift.start += delta;
        }
      }
    },
  },
  actions: {
    addPerson({ commit, state }) {
      let availableId = -1;
      let True = true;
      for (let i = 0; True; i++) {
        if (!state.people[i]) {
          availableId = i;
          break;
        }
      }

      let availableNum = -1;
      for (let i = 1; True; i++) {
        if (Object.values(state.people).every(p => p.num != i)) {
          availableNum = i;
          break;
        }
      }

      commit('addPerson', [availableId, availableNum]);
      return availableId;
    },
    duplicatePerson({ commit, state }, personId) {
      let availableId = -1;
      let True = true;
      for (let i = 0; True; i++) {
        if (!state.people[i]) {
          availableId = i;
          break;
        }
      }

      commit('duplicatePerson', [availableId, personId]);
      return availableId;
    },
    addTask({ commit, state }) {
      let availableId = -1;
      let True = true;
      for (let i = 0; True; i++) {
        if (!state.tasks[i]) {
          availableId = i;
          break;
        }
      }

      commit('addTask', availableId);
      return availableId;
    },
    duplicateTask({ commit, state }, taskId) {
      let availableId = -1;
      let True = true;
      for (let i = 0; True; i++) {
        if (!state.tasks[i]) {
          availableId = i;
          break;
        }
      }

      commit('duplicateTask', [availableId, taskId]);
      return availableId;
    },
    taskAddShift({ commit, state }, taskId) {
      let availableId = -1;
      let True = true;
      for (let i = 0; True; i++) {
        if (!state.tasks[taskId].shifts[i]) {
          availableId = i;
          break;
        }
      }

      commit('taskAddShift', [taskId, availableId]);
      return availableId;
    }
  }
});

export default store;

window.exampleData = function () {
  store.replaceState({
    tags: {
      0: "Soap allergy",
      1: "Driver's license",
    },
    people: {
      0: {
        num: 1,
        name: "Alice",
        phoneNum: "050-123-1234",
        tags: ["0", "1"],
        ident_color: 0,
      },
      1: {
        num: 2,
        name: "Bob",
        phoneNum: "050-123-1234",
        tags: ["1"],
        ident_color: 1,
      },
      2: {
        num: 3,
        name: "Candace",
        phoneNum: "050-123-1234",
        tags: ["1"],
        ident_color: 2,
      },
      3: {
        num: 4,
        name: "Dylan",
        phoneNum: "050-123-1234",
        tags: ["1"],
        ident_color: 3,
      },
      4: {
        num: 5,
        name: "Evan",
        phoneNum: "050-123-1234",
        tags: ["1"],
        ident_color: 4,
      },
      5: {
        num: 6,
        name: "Ferb",
        phoneNum: "050-123-1234",
        tags: ["1"],
        ident_color: 5,
      },
      6: {
        num: 7,
        name: "Gaben",
        phoneNum: "050-123-1234",
        tags: ["1"],
        ident_color: 0,
      },
      7: {
        num: 8,
        name: "Hermione",
        phoneNum: "050-123-1234",
        tags: [],
        ident_color: 1,
      },
      8: {
        num: 9,
        name: "Ivan",
        phoneNum: "050-123-1234",
        tags: [],
        ident_color: 2,
      },
      9: {
        num: 10,
        name: "Josh",
        phoneNum: "050-123-1234",
        tags: [],
        ident_color: 3,
      },
      10: {
        num: 11,
        name: "Karen",
        phoneNum: "050-123-1234",
        tags: [],
        ident_color: 4,
      },
      11: {
        num: 12,
        name: "Liam",
        phoneNum: "050-123-1234",
        tags: [],
        ident_color: 5,
      },
      12: {
        num: 13,
        name: "Max",
        phoneNum: "050-123-1234",
        tags: [],
        ident_color: 0,
      },
      13: {
        num: 14,
        name: "Noah",
        phoneNum: "050-123-1234",
        tags: [],
        ident_color: 1,
      },
      14: {
        num: 15,
        name: "Odin",
        phoneNum: "050-123-1234",
        tags: [],
        ident_color: 2,
      },
      15: {
        num: 16,
        name: "Peter",
        phoneNum: "050-123-1234",
        tags: [],
        ident_color: 3,
      },
    },
    tasks: {
      0: {
        name: "Clean dishes",
        description: "Clean each dish in the kitchen\n",
        difficulty: 3,
        mustHaveTags: [],
        mustNotHaveTags: ["0"],
        shifts: {
          0: { start: baseTime + timeMult * (12), duration: timeMult * (4), assigned: "1" },
          1: { start: baseTime + timeMult * (16), duration: timeMult * (3), assigned: null },
          2: { start: baseTime + timeMult * (24), duration: timeMult * (2), assigned: "1" },
          3: { start: baseTime + timeMult * (24+2), duration: timeMult * (2), assigned: null },
        },
      },
      1: {
        name: "Mow lawn",
        description: "The lawnmower is in the shed\n",
        difficulty: 3,
        mustHaveTags: [],
        mustNotHaveTags: [],
        shifts: {
          0: { start: baseTime + timeMult * (13), duration: timeMult * (4), assigned: null },
          1: { start: baseTime + timeMult * (14), duration: timeMult * (3), assigned: null },
          2: { start: baseTime + timeMult * (24+5), duration: timeMult * (1), assigned: null },
          3: { start: baseTime + timeMult * (24+6), duration: timeMult * (4), assigned: null },
        },
      },
      2: {
        name: "Wash clothes",
        description: "Use two spoons of detergent\n",
        difficulty: 3,
        mustHaveTags: [],
        mustNotHaveTags: [],
        shifts: {
          0: { start: baseTime + timeMult * (16), duration: timeMult * (3.5), assigned: null },
          1: { start: baseTime + timeMult * (16), duration: timeMult * (3.5), assigned: null },
          2: { start: baseTime + timeMult * (14.5), duration: timeMult * (5), assigned: null },
          3: { start: baseTime + timeMult * (24+6.25), duration: timeMult * (5), assigned: null },
          4: { start: baseTime + timeMult * (24+7), duration: timeMult * (4.75), assigned: null },
          5: { start: baseTime + timeMult * (24+7), duration: timeMult * (4.75), assigned: null },
        },
      },
      3: {
        name: "Paint shed",
        description: "Use paint #123, it's inside the shed\n",
        difficulty: 3,
        mustHaveTags: [],
        mustNotHaveTags: [],
        shifts: {
          0: { start: baseTime + timeMult * (23), duration: timeMult * (2), assigned: null },
        },
      },
      4: {
        name: "Buy groceries",
        description: "Go to GenericMart, buy:\n- Eggs\n- Bread\n- Sugar\n",
        difficulty: 3,
        mustHaveTags: ["1"],
        mustNotHaveTags: [],
        shifts: {
          0: { start: baseTime + timeMult * (17), duration: timeMult * (2), assigned: null },
          1: { start: baseTime + timeMult * (24+6), duration: timeMult * (2), assigned: null },
          2: { start: baseTime + timeMult * (24+10), duration: timeMult * (2), assigned: null },
        },
      },
      5: {
        name: "Buy soap",
        description: "Go to GenericMart, buy dish soap\n",
        difficulty: 3,
        mustHaveTags: ["1"],
        mustNotHaveTags: ["0"],
        shifts: {
          0: { start: baseTime + timeMult * (24+8.5), duration: timeMult * (1.5), assigned: null },
          1: { start: baseTime + timeMult * (24+10), duration: timeMult * (1.5), assigned: null },
        },
      },
    },
  });
}
