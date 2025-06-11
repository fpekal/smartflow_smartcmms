<template>
    <div class="header">
      <div class="logo-div">
        <Logo class="logo-img" />
      </div>
      <div class="logo-triangle"></div>
  
      <!-- Desktop buttons -->
      <div class="buttons-div">
        <RouterLink to="/"><v-btn class="button">Pulpit</v-btn></RouterLink>
        <RouterLink to="/protocols"><v-btn class="button">Protokoły</v-btn></RouterLink>
        <RouterLink to="/przeglady"><v-btn class="button">Przeglądy</v-btn></RouterLink>
      </div>
  
      <!-- Hamburger icon (mobile) -->
      <div class="hamburger" @click="menuOpen = !menuOpen">
        ☰
      </div>
    </div>
  
    <!-- Mobile dropdown menu -->
    <div class="mobile-menu" v-if="menuOpen">
      <RouterLink to="/" @click="menuOpen = false"><v-btn class="button">Pulpit</v-btn></RouterLink>
      <RouterLink to="/protocols" @click="menuOpen = false"><v-btn class="button">Protokoły</v-btn></RouterLink>
      <RouterLink to="/przeglady" @click="menuOpen = false"><v-btn class="button">Przeglądy</v-btn></RouterLink>
    </div>
  </template>
  
  <script setup>
    import { ref } from 'vue'
    import Logo from './Logo.vue'
    
    const menuOpen = ref(false)
  </script>
  
  <style scoped>
    .header {
        display: flex;
        align-items: center;
        height: 50px;
        width: 100%;
        background-color: var(--arsdeepblue);
        box-shadow: 2px 5px 5px 1px var(--lightlightgray);
        position: relative;
    }
    
    .logo-div {
        height: 100%;
        width: 300px;
        background-color: var(--white);
        display: flex;
        align-items: center;
    }
    
    .logo-triangle {
        height: 0;
        width: 0;
        border-left: 0px solid transparent;
        border-right: 30px solid transparent;
        border-top: 50px solid var(--white);
        background-color: var(--arsdeepblue);
    }
    
    .logo-img {
        height: calc(100% - 4px);
        padding: 2px 5px 2px 15px;
    }
    
    .buttons-div {
        padding-left: 50px;
        display: flex;
        gap: 10px;
    }
    
    .button {
        background-color: var(--white);
        color: var(--arsdeepblue);
    }
    
    .button:hover {
        background-color: var(--lightlightgray);
    }
    
    /* Hidden by default */
    .hamburger {
        display: none;
    }
  
  /* Responsive styles */
  @media (max-width: 768px) {
    .buttons-div {
      display: none;
    }
  
    .hamburger {
      display: block;
      color: var(--white);
      font-size: 24px;
      padding: 10px;
      cursor: pointer;
      margin-left: auto;
      margin-right: 15px;
    }
  
    .mobile-menu {
      position: absolute;
      top: 50px;
      right: 0;
      background-color: var(--white);
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
      display: flex;
      flex-direction: column;
      width: 200px;
      z-index: 1000;
    }
  
    .mobile-menu .button {
      width: 100%;
      justify-content: flex-start;
      border-bottom: 1px solid var(--lightlightgray);
    }
  }
  </style>
  