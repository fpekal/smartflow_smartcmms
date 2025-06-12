<template>
    <Header></Header>

    <Loading v-if="isLoading"></Loading>

    <div class="container">
      <h1>Nowy Protokół</h1>
  
      <form @submit.prevent="submit">
        <div class="form-group">
          <label>Imię i nazwisko autora</label>
          <input v-model="form.author_name" type="text" required />

          <label>ID Protokołu</label>
          <input v-model="form.id" type="text" required placeholder="np. 2.1.3" />
        </div>

        <div class="form-group">
          <label>Nazwa protokołu</label>
          <input v-model="form.name" type="text" required />
        </div>
  
        <div class="form-group">
          <label>Aktywności serwisowe</label>
          <div v-for="(activity, index) in form.fields.activities" :key="index" class="activity-row">
            <input v-model="form.fields.activities[index]" type="text" placeholder="Opis czynności" />
            <v-btn class="normal-button" type="button" @click="removeActivity(index)">Usuń</v-btn>
          </div>
          <v-btn class="normal-button" type="button" @click="addActivity">+ Dodaj aktywność</v-btn>
        </div>
  
        <v-btn class="normal-button" type="submit" :disabled="isLoading">
          {{ isLoading ? 'Tworzenie...' : 'Zatwierdź' }}
        </v-btn>
      </form>

    <RouterLink to="/protocols">
        <v-btn class="normal-button">Cofnij</v-btn>
    </RouterLink>
  
      <div v-if="error" class="error">
        <h2>Błąd:</h2>
        <p>{{ error }}</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { reactive, ref, inject } from 'vue'
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  const api = inject('cmms_api')
  const isLoading = ref(false);
  const error = ref('');

  const form = reactive({
    id: '',
    name: '',
    state: 1,
    fields: {
      activities: ['']
    }
  })
  
  const addActivity = () => {
    form.fields.activities.push('')
  }
  
  const removeActivity = (index) => {
    if (form.fields.activities.length > 1) {
      form.fields.activities.splice(index, 1)
    }
  }
  
  const submit = async () => {
    // Clear previous error
    error.value = ''
    
    if (!form.id.trim()) {
      error.value = 'ID protokołu jest wymagane'
      return
    }
    
    if (!form.name.trim()) {
      error.value = 'Nazwa protokołu jest wymagana'
      return
    }
    
    const filteredActivities = form.fields.activities.filter(activity => activity.trim() !== '')
    
    if (filteredActivities.length === 0) {
      error.value = 'Przynajmniej jedna aktywność jest wymagana'
      return
    }
    
    isLoading.value = true
    
    try {
      const protocol = {
        id: form.id.trim(),
        name: form.name.trim(),
        state: form.state,
        fields: {
          activities: filteredActivities
        }
      }

      await api.createProtocol(protocol)
      
      // Success - navigate back
      router.back()
      
    } catch (err) {
      console.error('Error creating protocol:', err)
      error.value = err.message || 'Wystąpił błąd podczas tworzenia protokołu'
    } finally {
      isLoading.value = false
    }
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
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
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
    align-items: center;
  }
  
  .activity-row input {
    flex: 1;
  }
  
  button {
    padding: 8px 16px;
    margin-top: 5px;
  }
  
  .error {
    background-color: #fee;
    border: 1px solid #fcc;
    padding: 15px;
    border-radius: 5px;
    margin-top: 20px;
  }
  
  .error h2 {
    color: #c33;
    margin-top: 0;
  }
  
  .error p {
    color: #c33;
    margin-bottom: 0;
  }
  </style>