<template>
  <div class="onboarding">
    <header class="mt-5 mb-5 mr-3 ml-3 d-flex flex-row align-items-center justify-content-center">
      <img class="logo_2x" alt="Samal to logo" src="../assets/logo_2x.png">
      <h1>Shift manager &amp; assigner</h1>
    </header>
    <h2>Guide</h2>
    <h3>1. Create tasks</h3>
    <p>Add a description for clarity, Add "Required" and "Disqualifying" tags to restrict assignment</p>
    <p>Create all shifts that need to be filled</p>
    <h3>2. Create people</h3>
    <p>Add contact info and tags to restrict assignment</p>
    <h3>3. Press "Auto Assign" in "Table"</h3>
    <p>In a couple of seconds you should have a fair timetable, press "Share PNG" to share it!</p>
    <center>
      <b-button
        @click="createRoom"
        class="mt-4 createbtn"
        variant="primary"
      >Create Room</b-button>
    </center>
    <footer>
      <em>
        All data is stored locally<br>
        Data is anonymized locally before auto-assigning on the server<br>
        Created by <a href="https://github.com/Wazzaps">@Wazzaps</a> and <a href="https://github.com/Itay2805">@Itay2805</a>
      </em>
    </footer>
  </div>
</template>

<script>
export default {
  methods: {
    createRoom() {
      const roomID = this.generateRandomID();
      localStorage.setItem(`state-${roomID}`, JSON.stringify({
        tags: {},
        people: {},
        tasks: {},
      }));
      this.$router.push(`/${roomID}/tasks`);
    },
    generateRandomID() {
      var idBytes = new Uint8Array([0, 0, 0, 0, 0, 0]);
      for (let i = 0; i < 6; i++) {
        idBytes[i] = Math.random() * 256;
      }
      return btoa(String.fromCharCode.apply(null, idBytes))
        .replace(/\+/g, "-")
        .replace(/\//g, "_");
    },
  },
};
</script>

<style scoped>
.logo_2x {
  height: 80px;
  box-shadow: 0 8px 32px -4px #6594c7;
  border-radius: 10px;
}

h1 {
  font-family: 'Rubik', sans-serif;
  font-weight: 400;
  color: #006cdf;
  margin: 0;
  font-size: 1.8rem;
}

h2 {
  font-family: 'Rubik', sans-serif;
  color: #006cdf;
  font-size: 1.6rem;
  margin-left: 1.5rem;
}

h3 {
  font-family: 'Rubik', sans-serif;
  font-weight: 400;
  color: #006cdf;
  font-size: 1.2rem;
  margin-left: 2.5rem;
}

p {
  font-size: 1.1rem;
  margin-left: 2.5rem;
  margin-right: 1rem;
}

.onboarding {
  max-width: 34rem;
  margin: auto;
}

.createbtn {
  padding: 0.6rem 1.6rem;
  font-size: 1.6rem;
  border-radius: 0.5rem;
}

footer {
  max-width: 15rem;
  margin: auto;
  margin-top: 2.5rem;
  text-align: center;
  color: #777;
  font-size: 0.8rem;
}

header img {
  margin-right: 2rem;
}
</style>