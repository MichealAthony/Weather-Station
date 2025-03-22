<template>
  <v-container fluid align="center" class="background">
    <v-row class="row1" max-width="1200px" justify="center" align="center" padding="1">
      <v-col class="col col1">
        <v-sheet class="pa-2 bg-background" height="250">
          <v-text-field
            label="Start date"
            type="date"
            density="compact"
            solo-inverted
            class="mr-5"
            max-width="300px"
            flat
            v-model="start"
          ></v-text-field>
          <v-text-field
            label="End date"
            type="date"
            density="compact"
            solo-inverted
            class="mr-5"
            max-width="300px"
            flat
            v-model="end"
          ></v-text-field>
          <v-spacer></v-spacer>
          <v-btn @click="updateLineCharts(); updateScatterCharts();" class="btn-analyze" text>
            Analyze
          </v-btn>
        </v-sheet>
      </v-col>
    </v-row>
    <v-row style="max-width: 1200px;">
      <!-- COLUMN 1 -->
      <v-col cols="6">
        <figure class="highcharts-figure">
          <div id="container"></div>
        </figure>
      </v-col>
      <!-- COLUMN 2 -->
      <v-col cols="6">
        <figure class="highcharts-figure">
          <div id="container0"></div>
        </figure>
      </v-col>
    </v-row>
    <v-row style="max-width: 1200px;">
      <!-- COLUMN 1 -->
      <v-col cols="6">
        <figure class="highcharts-figure">
          <div id="container1"></div>
        </figure>
      </v-col>
      <!-- COLUMN 2 -->
      <v-col cols="6">
        <figure class="highcharts-figure">
          <div id="container2"></div>
        </figure>
      </v-col>
      <!-- COLUMN 3 -->
      <v-col cols="12">
        <figure class="highcharts-figure">
          <div id="container3"></div>
        </figure>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import Highcharts from "highcharts";
import more from "highcharts/highcharts-more";
import Exporting from "highcharts/modules/exporting";
Exporting(Highcharts);
more(Highcharts);

import { onBeforeUnmount, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAppStore } from "@/store/appStore";
import { useMqttStore } from "@/store/mqttStore";
import { storeToRefs } from "pinia";

const Mqtt = useMqttStore();
const AppStore = useAppStore();
const router = useRouter();
const route = useRoute();
const { payload, payloadTopic } = storeToRefs(Mqtt);

var start = ref(null);
var end = ref(null);

const TempvsHumiLine = ref(null); // Chart object
const PressVsAltLine = ref(null); // Chart object
const SoilMoistureChart = ref(null);
const TempvsHILine   = ref(null);
const DHTvsBMPLine   = ref(null);

const CreateCharts = async () => {
  // TEMPERATURE vs. HUMIDITY CHART
  TempvsHumiLine.value = Highcharts.chart("container", {
    chart: { zoomType: "x" },
    title: { text: "Temperature vs. Humidity Analysis", align: "left" },
    yAxis: {
      title: { text: "Temperature", style: { color: "#000000" } },
      labels: { format: "{value} °C" }
    },
    xAxis: {
      title: { text: "Humidity", style: { color: "#000000" } },
      labels: { format: "{value} %" }
    },
    tooltip: {
      shared: true,
      pointFormat: 'Humidity: {point.x} % <br/> Temperature: {point.y} °C'
    },
    series: [
      {
        name: "Celsius Temperature",
        type: "line",
        data: [],
        turboThreshold: 0,
        color: Highcharts.getOptions().colors[2]
      },
      {
        name: "Humidity",
        type: "line",
        data: [],
        turboThreshold: 0,
        color: Highcharts.getOptions().colors[6]
      }
    ]
  });

  // PRESSURE vs. ALTITUDE CHART
  PressVsAltLine.value = Highcharts.chart("container2", {
    chart: { zoomType: "x" },
    title: { text: "Pressure and Altitude Correlation Analysis", align: "left" },
    yAxis: {
      title: { text: "Pressure", style: { color: "#000000" } },
      labels: { format: "{value} Pa" }
    },
    xAxis: {
      title: { text: "Altitude", style: { color: "#000000" } },
      labels: { format: "{value} m" }
    },
    tooltip: {
      shared: true,
      pointFormat: 'Altitude: {point.x} m <br/> Pressure: {point.y} Pa'
    },
    series: [
      {
        name: "Analysis",
        type: "spline",
        data: [],
        turboThreshold: 0,
        color: Highcharts.getOptions().colors[2]
      }
    ]
  });

  // DHT vs. BMP TEMPERATURE COMPARISON CHART
  DHTvsBMPLine.value = Highcharts.chart("container1", {
    chart: { zoomType: "x" },
    title: { text: "DHT Temperature and BMP Temperature Comparison", align: "left" },
    yAxis: {
      title: { text: "Temperature (°C)", style: { color: "#000000" } },
      labels: { format: "{value} °C" }
    },
    xAxis: {
      type: 'datetime',
      title: { text: 'Time', style: { color: '#000000' } }
    },
    tooltip: { shared: true },
    series: [
      {
        name: "DHT",
        type: "spline",
        data: [],
        turboThreshold: 0,
        color: Highcharts.getOptions().colors[6]
      },
      {
        name: "BMP",
        type: "spline",
        data: [],
        turboThreshold: 0,
        color: Highcharts.getOptions().colors[2]
      }
    ]
  });

  // TEMPERATURE & HEAT INDEX CHART
  TempvsHILine.value = Highcharts.chart("container0", {
    chart: { zoomType: 'x' },
    title: { text: 'Temperature & Heat Index Analysis', align: 'left' },
    subtitle: { 
      text: 'The heat index, also known as the "apparent temperature," is a measure that combines air temperature and relative humidity. As humidity increases, the heat index rises, making the perceived temperature higher than the actual air temperature.',
      align: 'left'
    },
    yAxis: {
      title: { text: 'Temperature', style: { color: '#000000' } },
      labels: { format: '{value} °C' }
    },
    xAxis: {
      type: 'datetime',
      title: { text: 'Heat Index', style: { color: '#000000' } },
      labels: { format: '{value} °F' }
    },
    tooltip: { 
      shared: true,
      pointFormat: 'Heat Index: {point.x} °F <br/> Temperature: {point.y} °C'
    },
    series: [
      {
        name: 'Analysis',
        type: 'spline',
        data: [],
        turboThreshold: 0,
        color: Highcharts.getOptions().colors[0]
      }
    ]
  });

  // SOIL MOISTURE ANALYSIS CHART
  SoilMoistureChart.value = Highcharts.chart('container3', {
    chart: { zoomType: 'x' },
    title: { text: 'Soil Moisture Analysis', align: 'left' },
    yAxis: {
      labels: { format: '{value} %' }
    },
    xAxis: {
      type: 'datetime',
      title: { text: 'Time', style: { color: '#000000' } }
    },
    tooltip: { shared: true },
    series: [
      {
        name: 'Soil Moisture',
        type: 'scatter',
        data: [],
        turboThreshold: 0,
        color: Highcharts.getOptions().colors[0]
      }
    ]
  });
};

onMounted(() => {
  // Connect to the MQTT broker on the backend
  Mqtt.connect();
  // Subscribe using the correct topics matching your hardware/backend
  setTimeout(() => {
    Mqtt.subscribe("620160532");
    Mqtt.subscribe("620160532_sub");
  }, 3000);
  CreateCharts();
});

onBeforeUnmount(() => {
  Mqtt.unsubcribeAll();
});

const updateLineCharts = async () => {
  if (!!start.value && !!end.value) {
    let startDate = new Date(start.value).getTime() / 1000;
    let endDate = new Date(end.value).getTime() / 1000;
    const data = await AppStore.getAllInRange(startDate, endDate);

    let celsTemperature = [];
    let bmp_temp = [];
    let tempvsHI = [];
    let tempvsHum = [];
    let pressvsAlt = [];

    data.forEach(row => {
      celsTemperature.push({ "x": row.timestamp * 1000, "y": parseFloat(row.celsTemperature.toFixed(2)) });
      bmp_temp.push({ "x": row.timestamp * 1000, "y": parseFloat(row.bmp_temp.toFixed(2)) });
      tempvsHI.push({ "x": parseFloat(row.heatindex.toFixed(2)), "y": parseFloat(row.celsTemperature.toFixed(2)) });
      tempvsHum.push({ "x": parseFloat(row.humidity.toFixed(2)), "y": parseFloat(row.celsTemperature.toFixed(2)) });
      pressvsAlt.push({ "x": parseFloat(row.altitude.toFixed(2)), "y": parseFloat(row.pressure.toFixed(2)) });
    });

    TempvsHILine.value.series[0].setData(tempvsHI);
    TempvsHumiLine.value.series[0].setData(tempvsHum);
    DHTvsBMPLine.value.series[0].setData(celsTemperature);
    DHTvsBMPLine.value.series[1].setData(bmp_temp);
    PressVsAltLine.value.series[0].setData(pressvsAlt);
  }
};

const updateScatterCharts = async () => {
  if (!!start.value && !!end.value) {
    let startDate = new Date(start.value).getTime() / 1000;
    let endDate = new Date(end.value).getTime() / 1000;
    const data = await AppStore.getAllInRange(startDate, endDate);

    let s1 = [];
    data.forEach(row => {
      s1.push({ "x": row.timestamp * 1000, "y": parseFloat(row.soilMoisture.toFixed(2)) });
    });

    SoilMoistureChart.value.series[0].setData(s1);
  }
};
</script>

<style scoped>
.background {
  background-color: #f0f2f5;
}

.v-btn.btn-analyze {
  background-color: #4caf50;
  color: white;
  font-weight: bold;
  border-radius: 8px;
  padding: 10px 20px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
}

.v-btn.btn-analyze:hover {
  background-color: #388e3c;
}

.highcharts-figure {
  margin: 0;
  padding: 0;
}

#container,
#container0,
#container1,
#container2,
#container3 {
  width: 100%;
  height: 400px;
}

.v-row {
  max-width: 1200px;
  width: 100%;
}

.v-col {
  padding: 1rem;
}

.sheet {
  padding: 2rem;
  height: 250px;
}
</style>
