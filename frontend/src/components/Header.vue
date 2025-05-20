<template>
    <div class="header">
        <div class="logo-div">
            <Logo class="logo-img"></Logo>
        </div>
        <div class="logo-triangle">
        </div>
        <div class="buttons-div">
            <RouterLink to="/"><v-btn class="button">Pulpit</v-btn></RouterLink>
            <RouterLink to="/protokoly"><v-btn class="button">Protokoły</v-btn></RouterLink>
            <RouterLink to="/przeglady"><v-btn class="button">Przeglądy</v-btn></RouterLink>
        </div>
    </div>
</template>

<script setup></script>

<style scoped>
    .header {
        display: flex;
        height: 50px;
        width: 100%;
        background-color: var(--arsdeepblue);
        align-items: center;
        box-shadow: 2px 5px 5px 1px var(--lightlightgray);
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
        padding-top: 2px;
        padding-bottom: 2px;
        padding-left: 15px;
        padding-right: 5px;
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
</style>