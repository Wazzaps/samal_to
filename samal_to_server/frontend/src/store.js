import Vuex from 'vuex'

// const pattern = 0;

const store = new Vuex.Store({
  state: {
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
        // ident_pattern: pattern,
      },
      1: {
        num: 2,
        name: "Bob",
        phoneNum: "050-123-1234",
        tags: ["1"],
        ident_color: 1,
        // ident_pattern: pattern,
      },
      2: {
        num: 3,
        name: "Candace",
        phoneNum: "050-123-1234",
        tags: ["1"],
        ident_color: 2,
        // ident_pattern: pattern,
      },
      3: {
        num: 4,
        name: "Dylan",
        phoneNum: "050-123-1234",
        tags: ["1"],
        ident_color: 3,
        // ident_pattern: pattern,
      },
      4: {
        num: 5,
        name: "Evan",
        phoneNum: "050-123-1234",
        tags: ["1"],
        ident_color: 4,
        // ident_pattern: pattern,
      },
      5: {
        num: 6,
        name: "Ferb",
        phoneNum: "050-123-1234",
        tags: ["1"],
        ident_color: 5,
        // ident_pattern: pattern,
      },
      6: {
        num: 7,
        name: "Gaben",
        phoneNum: "050-123-1234",
        tags: ["1"],
        ident_color: 0,
        // ident_pattern: pattern,
      },
      7: {
        num: 8,
        name: "Hermione",
        phoneNum: "050-123-1234",
        tags: [],
        ident_color: 1,
        // ident_pattern: pattern,
      },
      8: {
        num: 9,
        name: "Ivan",
        phoneNum: "050-123-1234",
        tags: [],
        ident_color: 2,
        // ident_pattern: pattern,
      },
      9: {
        num: 10,
        name: "Josh",
        phoneNum: "050-123-1234",
        tags: [],
        ident_color: 3,
        // ident_pattern: pattern,
      },
      10: {
        num: 11,
        name: "Karen",
        phoneNum: "050-123-1234",
        tags: [],
        ident_color: 4,
        // ident_pattern: pattern,
      },
      11: {
        num: 12,
        name: "Liam",
        phoneNum: "050-123-1234",
        tags: [],
        ident_color: 5,
        // ident_pattern: pattern,
      },
      12: {
        num: 13,
        name: "Max",
        phoneNum: "050-123-1234",
        tags: [],
        ident_color: 0,
        // ident_pattern: pattern,
      },
      13: {
        num: 14,
        name: "Noah",
        phoneNum: "050-123-1234",
        tags: [],
        ident_color: 1,
        // ident_pattern: pattern,
      },
      14: {
        num: 15,
        name: "Odin",
        phoneNum: "050-123-1234",
        tags: [],
        ident_color: 2,
        // ident_pattern: pattern,
      },
      15: {
        num: 16,
        name: "Peter",
        phoneNum: "050-123-1234",
        tags: [],
        ident_color: 3,
        // ident_pattern: pattern,
      },
    },
    tasks: {
      0: {
        name: "Clean dishes",
        description: "Clean each dish in the kitchen\n",
        mustHaveTags: [],
        mustNotHaveTags: ["0"],
        shifts: {
          0: { start: 12, duration: 4, assigned: null },
          1: { start: 16, duration: 3, assigned: null },
          2: { start: 24+6, duration: 1, assigned: null },
          3: { start: 24+11, duration: 1, assigned: null },
        },
      },
      1: {
        name: "Mow lawn",
        description: "The lawnmower is in the shed\n",
        mustHaveTags: [],
        mustNotHaveTags: [],
        shifts: {
          0: { start: 19, duration: 3, assigned: null },
          1: { start: 22, duration: 4, assigned: null },
          2: { start: 24+2, duration: 4, assigned: null },
          3: { start: 24+6, duration: 1, assigned: null },
        },
      },
      2: {
        name: "Wash clothes",
        description: "Use two spoons of detergent\n",
        mustHaveTags: [],
        mustNotHaveTags: [],
        shifts: {
          0: { start: 15, duration: 3.5, assigned: null },
          1: { start: 15, duration: 3.5, assigned: null },
          2: { start: 14.5, duration: 5, assigned: null },
          3: { start: 24+6.5, duration: 5, assigned: null },
          4: { start: 24+7, duration: 4.5, assigned: null },
          5: { start: 24+7, duration: 4.5, assigned: null },
        },
      },
      3: {
        name: "Paint shed",
        description: "Use paint #123, it's inside the shed\n",
        mustHaveTags: [],
        mustNotHaveTags: [],
        shifts: {
          0: { start: 21, duration: 2, assigned: null },
        },
      },
      4: {
        name: "Buy groceries",
        description: "Go to GenericMart, buy:\n- Eggs\n- Bread\n- Sugar\n",
        mustHaveTags: ["1"],
        mustNotHaveTags: [],
        shifts: {
          0: { start: 20, duration: 4, assigned: null },
          1: { start: 24, duration: 4, assigned: null },
          2: { start: 24+4, duration: 1, assigned: null },
        },
      },
      5: {
        name: "Buy soap",
        description: "Go to GenericMart, buy dish soap\n",
        mustHaveTags: ["1"],
        mustNotHaveTags: ["0"],
        shifts: {
          0: { start: 24+6+(5/6), duration: 2 + (1/6), assigned: null },
          1: { start: 24+5, duration: 2, assigned: null },
        },
      },
      6: {
        name: "Task A",
        description: "\n",
        mustHaveTags: [],
        mustNotHaveTags: [],
        shifts: {
          0: { start: 12, duration: 4, assigned: null },
          1: { start: 16, duration: 4, assigned: null },
          2: { start: 20, duration: 1, assigned: null },
        },
      },
      7: {
        name: "Task B",
        description: "\n",
        mustHaveTags: [],
        mustNotHaveTags: [],
        shifts: {
          0: { start: 24+4, duration: 2, assigned: null },
        },
      },
      8: {
        name: "Task C",
        description: "\n",
        mustHaveTags: [],
        mustNotHaveTags: [],
        shifts: {
          0: { start: 24+6, duration: 4, assigned: null },
          1: { start: 24+10, duration: 2, assigned: null },
        },
      },
      9: {
        name: "Task D",
        description: "\n",
        mustHaveTags: [],
        mustNotHaveTags: [],
        shifts: {
          0: { start: 24+7, duration: 3, assigned: null },
        },
      },
      10: {
        name: "Task E",
        description: "\n",
        mustHaveTags: [],
        mustNotHaveTags: [],
        shifts: {
          0: { start: 24+8 + (2/6), duration: (60 + 40) / 60, assigned: null },
        },
      },
      11: {
        name: "Task F",
        description: "\n",
        mustHaveTags: [],
        mustNotHaveTags: [],
        shifts: {
          0: { start: 20, duration: 4, assigned: null },
          1: { start: 24, duration: 4, assigned: null },
          2: { start: 24+4, duration: 1, assigned: null },
        },
      },
      12: {
        name: "Task G",
        description: "\n",
        mustHaveTags: [],
        mustNotHaveTags: [],
        shifts: {
          0: { start: 12, duration: 4, assigned: null },
          1: { start: 16, duration: 4, assigned: null },
          2: { start: 20, duration: 4, assigned: null },
          3: { start: 24, duration: 4, assigned: null },
          4: { start: 24+4, duration: 4, assigned: null },
          5: { start: 24+8, duration: 4, assigned: null },
        },
      },
    }
  },
  mutations: {
    // increment (state) {
    //   state.count++
    // }
    personAddTag(state, [personId, tagId]) {
      state.people[personId].tags.push(tagId);
    },

    personRemoveTag(state, [personId, tagId]) {
      state.people[personId].tags.splice(
        state.people[personId].tags.indexOf(tagId),
        1
      );
    },

    createTag(state, [tagId, tagName]) {
      state.tags[tagId] = tagName;
    },

    assignMultipleShifts(state, assignments) {
      assignments.forEach(([taskId, shiftId, personId]) => {
        state.tasks[taskId].shifts[shiftId].assigned = personId;
      })
    },
  }
});

export default store;