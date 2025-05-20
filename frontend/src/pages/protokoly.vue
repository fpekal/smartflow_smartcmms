<template>
    <Header></Header>
    
    <div class="buttons-div">
        <v-btn prepend-icon="mdi-plus" class="add-button"> DODAJ </v-btn>
        <v-btn prepend-icon="mdi-plus" class="import-button"> IMPORT </v-btn>
    </div>
    <v-divider :thickness="3" class="border-opacity-23"></v-divider>


</template>

<script setup>
</script>

<style scoped>
    .buttons-div {
        padding-left: 15px;
        padding-top: 15px;
        padding-bottom: 15px;
        display: flex;
        gap: 15px;
    }

    .add-button {
        background-color: var(--whitegray);
        color: var(--darkgray);
    }

    .import-button {
        background-color: var(--whitegray);
        color: var(--darkgray);
    }
</style>