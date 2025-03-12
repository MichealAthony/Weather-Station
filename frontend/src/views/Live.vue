<template>
    <div>
      <v-container fluid class="bg-background" align="center">
        <!-- ROW 1 -->
        <v-col justify="center" style="max-width: 1200px;">
          <v-card class="text-onPrimary" color="primaryContainer" style="max-width: 1200px; max-height: 800px;" flat>
            <h1>Temperature and Heat Index</h1>
          </v-card>
        </v-col>
        <v-row>
          <!-- COLUMN 1 -->
          <v-col cols="9">
            <figure class="highcharts-figure">
              <div id="container"></div>
            </figure>
          </v-col>
          <!-- COLUMN 2 -->
          <v-col cols="3">
            <v-card class="mb-5" style="max-width: 500px;" color="primaryContainer" subtitle="Celsius Temperature">
              <v-card-item>
                <span class="text-h2 text-onPrimaryContainer">{{ temperature }}</span>
                <v-btn @click="Tconvert()" text color="text-onPrimaryContainer" variant="tonal">
                  Convert
                </v-btn>
              </v-card-item>
            </v-card>
            <v-card class="mb-5" style="max-width: 500px;" color="background" subtitle="Heat Index (Feels like)">
              <v-card-item>
                <span class="text-h2 text-onSecondaryContainer">{{ heatindex }}</span>
              </v-card-item>
            </v-card>
          </v-col>
        </v-row>
        <!-- ROW 2 -->
        <v-col justify="center" style="max-width: 1200px;">
          <v-card class="mt-5 text-onPrimary" color="primaryContainer" style="max-width: 1200px; max-height: 800px;" flat>
            <h1>Humidity</h1>
          </v-card>
        </v-col>
        <v-row>
          <!-- COLUMN 1 -->
          <v-col cols="9">
            <figure class="highcharts-figure">
              <div id="container1"></div>
            </figure>
          </v-col>
          <!-- COLUMN 2 -->
          <v-col cols="3">
            <v-card color="primaryContainer">
              <v-card-item>
                <span class="text-h2 text-onPrimaryContainer">{{ humidity }}</span>
              </v-card-item>
            </v-card>
          </v-col>
        </v-row>
        <!-- ROW 3 -->
        <v-row>
          <v-col cols="6">
            <v-card class="mt-5 text-onPrimary" color="primaryContainer" style="max-width: 800px; max-height: 800px;" flat>
              <h1>Pressure</h1>
            </v-card>
            <v-card class="mt-4" style="max-width: 800px;" color="primaryContainer">
              <v-card-item>
                <span class="text-h2 text-onTertiaryContainer">{{ pressure }}</span>
              </v-card-item>
            </v-card>
          </v-col>
          <v-col cols="6">
            <v-card class="mt-5 text-onPrimary" color="primaryContainer" style="max-width: 800px; max-height: 800px;" flat>
              <h1>Approximate Altitude</h1>
            </v-card>
            <v-card class="mt-4" style="max-width: 800px;" color="primaryContainer">
              <v-card-item>
                <span class="text-h2 text-onTertiaryContainer">{{ altitude }}</span>
              </v-card-item>
            </v-card>
          </v-col>
        </v-row>
        <!-- ROW 4 -->
        <v-col justify="center" style="max-width: 1200px;">
          <v-card class="mt-5 text-onPrimary" color="primaryContainer" style="max-width: 1200px; max-height: 800px;" flat>
            <h1>Soil Moisture</h1>
          </v-card>
        </v-col>
        <v-row>
          <v-col cols="9">
            <figure class="highcharts-figure">
              <div id="container2"></div>
            </figure>
          </v-col>
          <v-col cols="3">
            <v-card class="mb-5" style="max-width: 500px;" color="background">
              <v-card-item>
                <v-sheet color="background" class="mt-5" width="200">
                  <span class="text-h2 text-onSecondaryContainer">{{ soilMoisture }}</span>
                  <v-slider color="primaryContainer" v-model="soilMoisture" max="100" thumb-label direction="vertical" track-size="60"></v-slider>
                </v-sheet>
              </v-card-item>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </template>
  
  <script setup>
  import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
  import { useRoute, useRouter } from "vue-router";
  import { useMqttStore } from "@/store/mqttStore";
  import { storeToRefs } from "pinia";
  import Highcharts from "highcharts";
  import more from "highcharts/highcharts-more";
  import Exporting from "highcharts/modules/exporting";
  Exporting(Highcharts);
  more(Highcharts);
  
  const router = useRouter();
  const route = useRoute();
  
  const Mqtt = useMqttStore();
  const { payload, payloadTopic } = storeToRefs(Mqtt);
  
  // Chart objects
  const tempHiChart = ref(null);
  const humiChart = ref(null);
  const soilChart = ref(null);
  
  // State variable for temperature unit conversion
  let Tstate = 0;
  
  const temperature = computed(() => {
    if (payload.value &&
        typeof payload.value.fahrTemperature === 'number' &&
        typeof payload.value.celsTemperature === 'number') {
      return Tstate === 1
        ? `${payload.value.fahrTemperature.toFixed(2)} °F`
        : `${payload.value.celsTemperature.toFixed(2)} °C`;
    }
    return "N/A";
  });
  
  const heatindex = computed(() => {
    if (payload.value && typeof payload.value.heatindex === 'number') {
      return `${payload.value.heatindex.toFixed(2)} °F`;
    }
    return "N/A";
  });
  
  const humidity = computed(() => {
    if (payload.value && typeof payload.value.humidity === 'number') {
      return `${payload.value.humidity.toFixed(2)} %`;
    }
    return "N/A";
  });
  
  const soilMoisture = computed(() => {
    if (payload.value && typeof payload.value.soilMoisture === 'number') {
      return `${payload.value.soilMoisture.toFixed(2)} %`;
    }
    return "N/A";
  });
  
  const pressure = computed(() => {
    if (payload.value && typeof payload.value.pressure === 'number') {
      return `${payload.value.pressure.toFixed(2)} Pa`;
    }
    return "N/A";
  });
  
  const altitude = computed(() => {
    if (payload.value && typeof payload.value.altitude === 'number') {
      return `${payload.value.altitude.toFixed(2)} m`;
    }
    return "N/A";
  });
  
  // FUNCTIONS
  const Tconvert = () => {
    Tstate = Tstate === 0 ? 1 : 0;
  };
  
  const CreateCharts = async () => {
    // TEMPERATURE CHART (Live)
    tempHiChart.value = Highcharts.chart("container", {
      chart: { zoomType: "x" },
      title: { text: "Temperature Analysis (Live)", align: "left" },
      yAxis: { labels: { format: "{value} °C" } },
      xAxis: {
        type: "datetime",
        title: { text: "Time", style: { color: "#000000" } }
      },
      tooltip: { shared: true },
      series: [
        {
          name: "Temperature",
          type: "spline",
          data: [],
          turboThreshold: 0,
          color: Highcharts.getOptions().colors[0]
        },
        {
          name: "Heat Index",
          type: "spline",
          data: [],
          turboThreshold: 0,
          color: Highcharts.getOptions().colors[1]
        }
      ]
    });
    // HUMIDITY CHART (Live)
    humiChart.value = Highcharts.chart("container1", {
      chart: { zoomType: "x" },
      title: { text: "Humidity Analysis (Live)", align: "left" },
      yAxis: { labels: { format: "{value} °C" } },
      xAxis: {
        type: "datetime",
        title: { text: "Time", style: { color: "#000000" } }
      },
      tooltip: { shared: true },
      series: [
        {
          name: "Humidity",
          type: "spline",
          data: [],
          turboThreshold: 0,
          color: Highcharts.getOptions().colors[1]
        }
      ]
    });
    // SOIL MOISTURE CHART (Live)
    soilChart.value = Highcharts.chart("container2", {
      chart: { zoomType: "x" },
      title: { text: "Soil Moisture Analysis (Live)", align: "left" },
      yAxis: { labels: { format: "{value} %" } },
      xAxis: {
        type: "datetime",
        title: { text: "Time", style: { color: "#000000" } }
      },
      tooltip: { shared: true },
      series: [
        {
          name: "Soil Moisture",
          type: "spline",
          data: [],
          turboThreshold: 0,
          color: Highcharts.getOptions().colors[0]
        }
      ]
    });
  };
  
  // WATCHERS
  watch(payload, (data) => {
    if (data) {
      tempHiChart.value.series[0].addPoint(
        { y: parseFloat(data.celsTemperature.toFixed(2)), x: data.timestamp * 1000 },
        true,
        false
      );
      tempHiChart.value.series[1].addPoint(
        { y: parseFloat(data.heatindex.toFixed(2)), x: data.timestamp * 1000 },
        true,
        false
      );
      humiChart.value.series[0].addPoint(
        { y: parseFloat(data.humidity.toFixed(2)), x: data.timestamp * 1000 },
        true,
        false
      );
      soilChart.value.series[0].addPoint(
        { y: parseFloat(data.soilMoisture.toFixed(2)), x: data.timestamp * 1000 },
        true,
        false
      );
    }
  });
  
  onMounted(() => {
    CreateCharts();
    Mqtt.connect(); // Connect to the backend MQTT broker
    // Updated subscription topics to "620160532" and "620160532_pub" to match backend configuration.
    setTimeout(() => {
      Mqtt.subscribe("620160532");
      Mqtt.subscribe("620160532_pub");
    }, 3000);
  });
  
  onBeforeUnmount(() => {
    Mqtt.unsubcribeAll();
  });
  </script>
  
  <style scoped>
  figure {
    border: 2px solid green;
  }
  </style>
  