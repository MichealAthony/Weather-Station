<template>
  <VContainer class="fill-height stylish-container">
    <VRow class="d-flex justify-center align-center fill-height">
      <VCol cols="auto">
        <VCard class="elevated-card" elevation="8">
          <VCardText>
            <!-- Logo Image with Animation -->
            <VImg height="180" class="mb-5 fade-in" src="@/assets/logo.svg" />

            <!-- Welcome Message -->
            <div class="text-body-2 font-weight-light mb-2 text-white">Welcome to</div>
            <h1 class="text-h2 font-weight-bold text-gradient">Rohan Brown's</h1>
            <div class="text-body-1 font-weight-light mt-1 text-white">Remote Weather Station Platform</div>

            <!-- Weather Icons Section -->
            <VRow class="d-flex align-center justify-center mt-6">
              <VCol cols="auto">
                <VIcon class="weather-icon" icon="mdi-weather-sunny" size="48" />
                <div class="mt-2">Sunny</div>
              </VCol>

              <VCol cols="auto">
                <VIcon class="weather-icon" icon="mdi-weather-cloudy" size="48" />
                <div class="mt-2">Cloudy</div>
              </VCol>

              <VCol cols="auto">
                <VIcon class="weather-icon" icon="mdi-weather-rainy" size="48" />
                <div class="mt-2">Rainy</div>
              </VCol>
            </VRow>

            <!-- Button Section -->
            <VRow class="d-flex align-center justify-center mt-6">
              <VCol cols="auto">
                <VBtn
                  href="https://vuetifyjs.com/components/all/"
                  rel="noopener noreferrer"
                  target="_blank"
                  variant="outlined"
                  class="animated-button"
                >
                  <VIcon icon="mdi-view-dashboard" size="large" start />
                  Components
                </VBtn>
              </VCol>

              <VCol cols="auto">
                <VBtn
                  color="primary"
                  href="https://vuetifyjs.com/introduction/why-vuetify/#feature-guides"
                  rel="noopener noreferrer"
                  size="x-large"
                  target="_blank"
                  variant="elevated"
                  class="animated-button primary-btn"
                >
                  <VIcon icon="mdi-speedometer" size="large" start />
                  Get Started
                </VBtn>
              </VCol>

              <VCol cols="auto">
                <VBtn
                  href="https://community.vuetifyjs.com/"
                  rel="noopener noreferrer"
                  target="_blank"
                  variant="outlined"
                  class="animated-button"
                >
                  <VIcon icon="mdi-account-group" size="large" start />
                  Community
                </VBtn>
              </VCol>
            </VRow>
          </VCardText>
        </VCard>
      </VCol>
    </VRow>
  </VContainer>
</template>

<script setup>
import { onMounted, onBeforeUnmount } from 'vue';

onMounted(() => {});

onBeforeUnmount(() => {});
</script>

<style scoped>
/* Apply styles to the whole page */
.stylish-container {
  background: linear-gradient(135deg, #1e3c72, #2a5298);
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

/* Card Styling */
.elevated-card {
  max-width: 600px;
  width: 100%; /* Ensure the card takes full available width */
  padding: 32px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease-in-out;
  text-align: center;
}

.elevated-card:hover {
  transform: translateY(-5px);
}

/* Text Gradient */
.text-gradient {
  background: linear-gradient(45deg, #ff8a00, #e52e71);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* White Text */
.text-white {
  color: white !important;
}

/* Weather Icons */
.weather-icon {
  color: #ff8a00; /* Custom color for icons */
}

/* Button Animations */
.animated-button {
  transition: all 0.3s ease-in-out;
  border: 2px solid white;
  color: white !important;
}

.animated-button:hover {
  transform: scale(1.1);
  background: white;
  color: #2a5298 !important;
}

/* Primary Button */
.primary-btn {
  background-color: #ff8a00 !important;
  color: white !important;
}

/* Image Animation */
.fade-in {
  opacity: 0;
  animation: fadeIn 1s forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
