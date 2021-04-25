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
        tags: ["0"],
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
        tags: [],
        ident_color: 3,
        // ident_pattern: pattern,
      },
      4: {
        num: 5,
        name: "Evan",
        phoneNum: "050-123-1234",
        tags: [],
        ident_color: 4,
        // ident_pattern: pattern,
      },
      5: {
        num: 6,
        name: "Ferb",
        phoneNum: "050-123-1234",
        tags: [],
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
    },
    tasks: {
      0: {
        name: "Clean dishes",
        description: "Clean each dish in the kitchen\n",
        mustHaveTags: [],
        mustNotHaveTags: ["0"],
        shifts: {
          0: {start: 0, duration: 5, assigned: "3"},
          1: {start: 5, duration: 3, assigned: null},
        },
      },
      1: {
        name: "Mow lawn",
        description: "The lawnmower is in the shed\n",
        mustHaveTags: [],
        mustNotHaveTags: [],
        shifts: {},
      },
      2: {
        name: "Wash clothes",
        description: "Use two spoons of detergent\n",
        mustHaveTags: [],
        mustNotHaveTags: ["0"],
        shifts: {},
      },
      3: {
        name: "Paint shed",
        description: "Use paint #123, it's inside the shed\n",
        mustHaveTags: [],
        mustNotHaveTags: [],
        shifts: {},
      },
      4: {
        name: "Buy groceries",
        description: "Go to GenericMart, buy:\n- Eggs\n- Bread\n- Sugar\n",
        mustHaveTags: ["1"],
        mustNotHaveTags: [],
        shifts: {},
      },
      5: {
        name: "Buy soap",
        description: "Go to GenericMart, buy dish soap\n",
        mustHaveTags: ["1"],
        mustNotHaveTags: ["0"],
        shifts: {},
      },
    }
  },
  mutations: {
    // increment (state) {
    //   state.count++
    // }
    personAddTag (state, [personId, tagId]) {
      state.people[personId].tags.push(tagId);
    },

    personRemoveTag (state, [personId, tagId]) {
      state.people[personId].tags.splice(
        state.people[personId].tags.indexOf(tagId),
        1
      );
    },

    createTag (state, [tagId, tagName]) {
      state.tags[tagId] = tagName;
    }
  }
});

export default store;