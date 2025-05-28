<template>
    <Header></Header>
    
    <div class="buttons-div">
        <v-btn prepend-icon="mdi-plus" class="normal-button"> DODAJ </v-btn>
        <v-btn prepend-icon="mdi-plus" class="normal-button" @click="importProtocols"> IMPORT </v-btn>
    </div>
    <v-divider :thickness="3" class="border-opacity-23"></v-divider>

    <div class="protocols-div">
        <RouterLink class="protocols-div" v-for="p in protocols" :to="'/protocol/' + p.id">
            <v-btn class="protocol-button">{{ p.name }}</v-btn>
        </RouterLink>
        <v-btn class="protocol-button">test</v-btn>
        <v-btn class="protocol-button">test</v-btn>
        <v-btn class="protocol-button">test</v-btn>
    </div>
</template>

<script setup>
    import {inject, ref} from 'vue'

    let api = inject('cmms_api')
    let protocols = ref([]);

    async function importProtocols() {
        protocols.value = (await api.getProtocols()).data
    }
</script>

<style scoped>
    .buttons-div {
        padding-left: 15px;
        padding-top: 15px;
        padding-bottom: 15px;
        display: flex;
        gap: 15px;
    }

    .protocols-div {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 15px;
        margin-top: 15px;
    }

    .normal-button {
        background-color: var(--whitegray);
        color: var(--darkgray);
    }

    .protocol-button {
        background-color: var(--whitegray);
        color: var(--darkgray);
        width: 95%;
        justify-content: left;
        text-transform: none;
    }
</style>