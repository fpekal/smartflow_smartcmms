<template>
    <div class="loading-overlay">
      <div class="loading-container">
        <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
        <p class="loading-text">Ładowanie...</p>
      </div>
    </div>
  </template>
  
  <script setup>
  // No specific script needed here, it’s a static loading screen
  </script>
  
  <style scoped>
  .loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
  }
  
  .loading-container {
    text-align: center;
    color: #fff;
  }
  
  .loading-text {
    margin-top: 16px;
    font-size: 18px;
    font-weight: bold;
  }
  </style>
  