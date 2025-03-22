<template>
  <div>
    <v-container fluid class="bg-background" align="center">
      <!-- ROW 1: Temperature and Heat Index -->
      <v-col justify="center" style="max-width: 1200px;">
        <v-card class="text-onPrimary" color="deep-purple accent-4" style="max-width: 1200px; max-height: 800px;" flat>
          <v-row class="d-flex align-center">
            <v-col cols="auto">
              <v-icon size="40" class="text-white">mdi-thermometer</v-icon>
            </v-col>
            <v-col>
              <h1 class="text-white">Temperature and Heat Index</h1>
            </v-col>
          </v-row>
        </v-card>
      </v-col>

      <v-row>
        <!-- COLUMN 1: Temperature Chart -->
        <v-col cols="9">
          <figure class="highcharts-figure">
            <div id="container"></div>
          </figure>
        </v-col>
        <!-- COLUMN 2: Temperature and Heat Index -->
        <v-col cols="3">
          <v-card class="mb-5" style="max-width: 500px;" color="deep-purple accent-3" subtitle="Celsius Temperature">
            <v-card-item>
              <span class="text-h2 text-onSecondary">{{ temperature }}</span>
              <v-btn @click="Tconvert()" text color="text-onSecondary" variant="tonal">
                Convert
              </v-btn>
            </v-card-item>
          </v-card>
          <v-card class="mb-5" style="max-width: 500px;" color="deep-purple lighten-2" subtitle="Heat Index (Feels like)">
            <v-card-item>
              <span class="text-h2 text-onSecondary">{{ heatindex }}</span>
            </v-card-item>
          </v-card>
        </v-col>
      </v-row>

      <!-- ROW 2: Humidity -->
      <v-col justify="center" style="max-width: 1200px;">
        <v-card class="mt-5 text-onPrimary" color="blue-grey darken-3" style="max-width: 1200px; max-height: 800px;" flat>
          <v-row class="d-flex align-center">
            <v-col cols="auto">
              <v-icon size="40" class="text-white">mdi-water-percent</v-icon>
            </v-col>
            <v-col>
              <h1 class="text-white">Humidity</h1>
            </v-col>
          </v-row>
        </v-card>
      </v-col>

      <v-row>
        <!-- COLUMN 1: Humidity Chart -->
        <v-col cols="9">
          <figure class="highcharts-figure">
            <div id="container1"></div>
          </figure>
        </v-col>
        <!-- COLUMN 2: Humidity Value -->
        <v-col cols="3">
          <v-card color="blue-grey lighten-3">
            <v-card-item>
              <span class="text-h2 text-onPrimary">{{ humidity }}</span>
            </v-card-item>
          </v-card>
        </v-col>
      </v-row>

      <!-- ROW 3: Pressure and Altitude -->
      <v-row>
        <v-col cols="6">
          <v-card class="mt-5 text-onPrimary" color="teal darken-4" style="max-width: 800px; max-height: 800px;" flat>
            <v-row class="d-flex align-center">
              <v-col cols="auto">
                <v-icon size="40" class="text-white">mdi-gauge</v-icon>
              </v-col>
              <v-col>
                <h1 class="text-white">Pressure</h1>
              </v-col>
            </v-row>
          </v-card>
          <v-card class="mt-4" style="max-width: 800px;" color="teal lighten-2">
            <v-card-item>
              <span class="text-h2 text-onTertiary">{{ pressure }}</span>
            </v-card-item>
          </v-card>
        </v-col>

        <v-col cols="6">
          <v-card class="mt-5 text-onPrimary" color="amber darken-4" style="max-width: 800px; max-height: 800px;" flat>
            <v-row class="d-flex align-center">
              <v-col cols="auto">
                <v-icon size="40" class="text-white">mdi-altimeter</v-icon>
              </v-col>
              <v-col>
                <h1 class="text-white">Approximate Altitude</h1>
              </v-col>
            </v-row>
          </v-card>
          <v-card class="mt-4" style="max-width: 800px;" color="amber lighten-2">
            <v-card-item>
              <span class="text-h2 text-onTertiary">{{ altitude }}</span>
            </v-card-item>
          </v-card>
        </v-col>
      </v-row>

      <!-- ROW 4: Soil Moisture -->
      <v-col justify="center" style="max-width: 1200px;">
        <v-card class="mt-5 text-onPrimary" color="green darken-4" style="max-width: 1200px; max-height: 800px;" flat>
          <v-row class="d-flex align-center">
            <v-col cols="auto">
              <v-icon size="40" class="text-white">mdi-water-pump</v-icon>
            </v-col>
            <v-col>
              <h1 class="text-white">Soil Moisture</h1>
            </v-col>
          </v-row>
        </v-card>
      </v-col>

      <v-row>
        <!-- COLUMN 1: Soil Moisture Chart -->
        <v-col cols="9">
          <figure class="highcharts-figure">
            <div id="container2"></div>
          </figure>
        </v-col>
        <!-- COLUMN 2: Soil Moisture Value -->
        <v-col cols="3">
          <v-card class="mb-5" style="max-width: 500px;" color="green lighten-2">
            <v-card-item>
              <v-sheet color="green lighten-1" class="mt-5" width="200">
                <span class="text-h2 text-onPrimary">{{ soilMoisture }}</span>
                <v-slider color="green lighten-2" v-model="soilMoisture" max="100" thumb-label direction="vertical" track-size="60"></v-slider>
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
    yAxis: { labels: { format: "{value} %"} },
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
        color: Highcharts.getOptions().colors[2]
      }
    ]
  });
};
</script>
