<template>
    <Header></Header>
    
    <div class="buttons-div">
        <v-btn prepend-icon="mdi-plus" class="normal-button"> DODAJ </v-btn>
        <v-btn prepend-icon="mdi-upload" class="normal-button" @click="triggerFileUpload"> IMPORT </v-btn>
        <input
            ref="fileInput"
            type="file"
            style="display: none;"
            @change="uploadFile"
            accept=".json,.csv,.xlsx"
        />
    </div>
    <v-divider :thickness="3" class="border-opacity-23"></v-divider>

    <div class="protocols-div">
        <RouterLink class="protocols-div" v-for="p in protocols" :to="'/protocol/' + p.id">
            <v-btn class="protocol-button">{{ p.name }}</v-btn>
        </RouterLink>
    </div>

    
</template>

<script setup>
    import {inject, ref, onMounted} from 'vue'

    let api = inject('cmms_api')
    let protocols = ref([]);
    const fileInput = ref(null);

    async function importProtocols() {
        protocols.value = (await api.getProtocols()).data
    }

    function triggerFileUpload() {
        fileInput.value.click();
    }

    async function uploadFile(event) {
        const file = event.target.files[0];
        if (!file) return;

        try {
            const response = await api.uploadProtocols(file);
            
            if (response.error) {
                console.error('Upload failed:', response.error);
            } else {
                await importProtocols();
                event.target.value = '';
                console.log('File uploaded successfully:', response.message || 'Success');
            }
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    }

    onMounted(() => {
        importProtocols()
    })
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