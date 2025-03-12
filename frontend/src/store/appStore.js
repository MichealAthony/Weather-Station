import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore(
  'app',
  () => {
    /*  
      The composition API way of defining a Pinia store.
      ref() become state properties,
      computed() become getters,
      and functions become actions.
    */

    const getAllInRange = async (start, end) => {
      // FETCH REQUEST WILL TIMEOUT AFTER 60 SECONDS
      const controller = new AbortController();
      const signal = controller.signal;
      const id = setTimeout(() => {
        controller.abort();
      }, 60000);
      const URL = `/api/weatherstation/get/${start}/${end}`;
      try {
        const response = await fetch(URL, { method: 'GET', signal: signal });
        if (response.ok) {
          const data = await response.json();
          let keys = Object.keys(data);
          if (keys.includes("status")) {
            if (data["status"] == "found") {
              console.log(data["data"]);
              return data["data"];
            }
            if (data["status"] == "failed") {
              console.log("getAllInRange returned no data");
            }
          }
        } else {
          const data = await response.text();
          console.log(data);
        }
      } catch (err) {
        console.error('getAllInRange error: ', err.message);
      }
      return [];
    };

    const gettemperatureMMAR = async (start, end) => {
      // FETCH REQUEST WILL TIMEOUT AFTER 60 SECONDS
      const controller = new AbortController();
      const signal = controller.signal;
      const id = setTimeout(() => {
        controller.abort();
      }, 60000);
      const URL = `/api/mmar/temperature/${start}/${end}`;
      try {
        const response = await fetch(URL, { method: 'GET', signal: signal });
        if (response.ok) {
          const data = await response.json();
          let keys = Object.keys(data);
          if (keys.includes("status")) {
            if (data["status"] == "found") {
              console.log(data["data"]);
              return data["data"];
            }
            if (data["status"] == "failed") {
              console.log("gettemperatureMMAR returned no data");
            }
          }
        } else {
          const data = await response.text();
          console.log(data);
        }
      } catch (err) {
        console.error('gettemperatureMMAR error: ', err.message);
      }
      return [];
    };

    const gethumidityMMAR = async (start, end) => {
      // FETCH REQUEST WILL TIMEOUT AFTER 60 SECONDS
      const controller = new AbortController();
      const signal = controller.signal;
      const id = setTimeout(() => {
        controller.abort();
      }, 60000);
      const URL = `/api/mmar/humidity/${start}/${end}`;
      try {
        const response = await fetch(URL, { method: 'GET', signal: signal });
        if (response.ok) {
          const data = await response.json();
          let keys = Object.keys(data);
          if (keys.includes("status")) {
            if (data["status"] == "found") {
              console.log(data["data"]);
              return data["data"];
            }
            if (data["status"] == "failed") {
              console.log("gethumidityMMAR returned no data");
            }
          }
        } else {
          const data = await response.text();
          console.log(data);
        }
      } catch (err) {
        console.error('gethumidityMMAR error: ', err.message);
      }
      return [];
    };

    const getpressureMMAR = async (start, end) => {
      const controller = new AbortController();
      const signal = controller.signal;
      const id = setTimeout(() => {
        controller.abort();
      }, 60000);
      // Updated endpoint to match backend (lowercase 'pressure')
      const URL = `/api/mmar/pressure/${start}/${end}`;
      try {
        const response = await fetch(URL, { method: 'GET', signal: signal });
        if (response.ok) {
          const data = await response.json();
          let keys = Object.keys(data);
          if (keys.includes("status")) {
            if (data["status"] === "found") {
              console.log(data["data"]);
              return data["data"];
            }
            if (data["status"] === "failed") {
              console.log("getpressureMMAR returned no data");
            }
          }
        } else {
          const data = await response.text();
          console.log(data);
        }
      } catch (err) {
        console.error('getpressureMMAR error: ', err.message);
      }
      return [];
    };

    const getaltitudeMMAR = async (start, end) => {
      // FETCH REQUEST WILL TIMEOUT AFTER 60 SECONDS
      const controller = new AbortController();
      const signal = controller.signal;
      const id = setTimeout(() => {
        controller.abort();
      }, 60000);
      const URL = `/api/mmar/altitude/${start}/${end}`;
      try {
        const response = await fetch(URL, { method: 'GET', signal: signal });
        if (response.ok) {
          const data = await response.json();
          let keys = Object.keys(data);
          if (keys.includes("status")) {
            if (data["status"] == "found") {
              console.log(data["data"]);
              return data["data"];
            }
            if (data["status"] == "failed") {
              console.log("getaltitudeMMAR returned no data");
            }
          }
        } else {
          const data = await response.text();
          console.log(data);
        }
      } catch (err) {
        console.error('getaltitudeMMAR error: ', err.message);
      }
      return [];
    };

    const getsoilmoistureMMAR = async (start, end) => {
      // FETCH REQUEST WILL TIMEOUT AFTER 60 SECONDS
      const controller = new AbortController();
      const signal = controller.signal;
      const id = setTimeout(() => {
        controller.abort();
      }, 60000);
      const URL = `/api/mmar/soilmoisture/${start}/${end}`;
      try {
        const response = await fetch(URL, { method: 'GET', signal: signal });
        if (response.ok) {
          const data = await response.json();
          let keys = Object.keys(data);
          if (keys.includes("status")) {
            if (data["status"] == "found") {
              console.log(data["data"]);
              return data["data"];
            }
            if (data["status"] == "failed") {
              console.log("getsoilmoistureMMAR returned no data");
            }
          }
        } else {
          const data = await response.text();
          console.log(data);
        }
      } catch (err) {
        console.error('getsoilmoistureMMAR error: ', err.message);
      }
      return [];
    };

    const getFreqDistro = async (variable, start, end) => {
      // FETCH REQUEST WILL TIMEOUT AFTER 60 SECONDS
      const controller = new AbortController();
      const signal = controller.signal;
      const id = setTimeout(() => {
        controller.abort();
      }, 60000);
      const URL = `/api/frequency/${variable}/${start}/${end}`;
      try {
        const response = await fetch(URL, { method: 'GET', signal: signal });
        if (response.ok) {
          const data = await response.json();
          let keys = Object.keys(data);
          if (keys.includes("status")) {
            if (data["status"] == "found") {
              console.log(data["data"]);
              return data["data"];
            }
            if (data["status"] == "failed") {
              console.log("getFreqDistro returned no data");
            }
          }
        } else {
          const data = await response.text();
          console.log(data);
        }
      } catch (err) {
        console.error('getFreqDistro error: ', err.message);
      }
      return [];
    };

    // STATES (if needed, add your reactive state variables here)

    // ACTIONS (your functions defined above serve as actions)

    return {
      // EXPORTS
      getAllInRange,
      gettemperatureMMAR,
      gethumidityMMAR,
      getsoilmoistureMMAR,
      getpressureMMAR,
      getaltitudeMMAR,
      getFreqDistro,
    };
  },
  { persist: true }
);
