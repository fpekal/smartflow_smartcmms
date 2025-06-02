<template>
    <Header></Header>
    <div class="container">
      <h1>Nowy Protokół</h1>
  
      <form @submit.prevent="submit">
        <div class="form-group">
          <label>Nazwa protokołu</label>
          <input v-model="form.name" type="text" required />
        </div>

        <div class="form-group">
            <label>Imię i nazwisko autora</label>
            <input v-model="form.author_name" type="text" required />
        </div>
  
        <div class="form-group">
          <label>Aktywności serwisowe</label>
          <div v-for="(activity, index) in form.fields.activities" :key="index" class="activity-row">
            <input v-model="form.fields.activities[index]" type="text" placeholder="Opis czynności" />
            <v-btn class="normal-button" type="button" @click="removeActivity(index)">Usuń</v-btn>
          </div>
          <v-btn class="normal-button" type="button" @click="addActivity">+ Dodaj aktywność</v-btn>
        </div>
  
        <v-btn class="normal-button" type="submit">Zatwierdź</v-btn>
      </form>

    <RouterLink to="/protocols">
        <v-btn class="normal-button" type="submit">Cofnij</v-btn>
    </RouterLink>
  
      <div v-if="output" class="output">
        <h2>Wynik JSON:</h2>
        <pre>{{ output }}</pre>
      </div>
    </div>
    <Loading v-if="isLoading"></Loading>
  </template>
  
  <script setup>
  import { reactive, ref, inject } from 'vue'
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  const api = inject('cmms_api')
  const isLoading = ref(false);

  const form = reactive({
    name: '',
    author_id: null,
    author_name: '',
    state: 1,
    fields: {
      activities: ['']
    }
  })
  
  const output = ref('')
  
  const addActivity = () => {
    form.fields.activities.push('')
  }
  
  const removeActivity = (index) => {
    form.fields.activities.splice(index, 1)
  }
  
  const submit = () => {
    isLoading.value = true;
    const protocol = {
      id: 0,
      name: form.name,
      author_id: form.author_id,
      author_name: form.author_name,
      state: form.state,
      fields: {
        activities: [...form.fields.activities]
      }
    }

    api.createProtocol(protocol);
    isLoading.value = false;
    router.back();
  }
  </script>
  
  <style scoped>
  .container {
    max-width: 800px;
    margin: 30px auto;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  input[type="text"],
  input[type="number"] {
    width: 100%;
    padding: 8px;
    margin-top: 4px;
    box-sizing: border-box;
    border: 1px solid gray;
    border-radius: 5px;
  }
  
  .activity-row {
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
  }
  
  button {
    padding: 8px 16px;
    margin-top: 5px;
  }
  
  </style>
  