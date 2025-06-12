<template>
    <Header />

    <Loading v-if="isLoading"></Loading>

    <div v-if="protocol" class="protocol">
      <h1>{{ protocol.name }}</h1>
      <p>Autor: {{ protocol.author_name }}</p>

      <form @submit.prevent="submitForm">
        <table>
          <tbody>
            <tr>
              <td>Obiekt</td>
              <td><input v-model="form.building" type="text" /></td>
            </tr>
            <tr>
              <td>Adres</td>
              <td><input v-model="form.address" type="text" /></td>
            </tr>
            <tr>
              <td>Urządzenie / ilość</td>
              <td><input v-model="form.device" type="text" /></td>
            </tr>
            <tr>
              <td>Producent / Typ / Numer seryjny</td>
              <td><input v-model="form.model" type="text" /></td>
            </tr>
            <tr>
              <td>Lokalizacja urządzenia</td>
              <td><input v-model="form.localization" type="text" /></td>
            </tr>
            <tr>
              <td>Rodzaj przeglądu</td>
              <td>
                <select v-model="form.survey_freq">
                  <option value="Roczny">Roczny</option>
                  <option value="Półroczny">Półroczny</option>
                  <option value="Miesięczny">Miesięczny</option>
                  <option value="n/a">n/a</option>
                </select>
              </td>
            </tr>
            <tr>
              <td>Data wykonania</td>
              <td><input v-model="form.date" type="date" /></td>
            </tr>
          </tbody>
        </table>

        <p>Przed rozpoczęciem prac należy:</p>
        <ol>
            <li>zapoznać się z DTR urządzenia oraz dokumentacją techniczną</li>
            <li>sprawdzić narzędzia robocze, zabezpieczenia ogólne i osobiste (BHP)</li>
            <li>skutecznie zabezpieczyć miejsce prowadzenia prac przed dostępem osób postronnych</li>
        </ol>

        <br>

        <h3>Czynności serwisowe:</h3>
        <table class="service-activities">
          <thead>
            <tr>
              <th>Lp.</th>
              <th>Czynność</th>
              <th>Nie dotyczy</th>
              <th>Brak uchybień</th>
              <th>Uwagi</th>
              <th>Nie wykonano</th>
              <th>Komentarz</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(activity, index) in protocol.fields.activities" :key="index">
              <td>{{ index + 1 }}</td>
              <td>{{ activity }}</td>
              <td class="activity-radio">
                <input type="radio" :name="`activity_choice${index}`" value="nie_dotyczy" v-model="form.activities[index].choice" />
              </td>
              <td class="activity-radio">
                <input type="radio" :name="`activity_choice${index}`" value="brak_uchybień" v-model="form.activities[index].choice" />
              </td>
              <td class="activity-radio">
                <input type="radio" :name="`activity_choice${index}`" value="uwagi" v-model="form.activities[index].choice" />
              </td>
              <td class="activity-radio">
                <input type="radio" :name="`activity_choice${index}`" value="nie_wykonano" v-model="form.activities[index].choice" />
              </td>
              <td><textarea v-model="form.activities[index].comment" class="comment-text" /></td>
            </tr>
          </tbody>
        </table>

        <h3>Status urządzenia:</h3>
        <div>
          <label class="crossout">
            <input type="checkbox" v-model="form.operational" /> Sprawne
          </label>
          /
          <label class="crossout">
            <input type="checkbox" v-model="form.non_operational" /> Niesprawne
          </label>
        </div>
        <div>
          <label class="crossout">
            <input type="checkbox" v-model="form.allowed" /> Dopuszczone do dalszej eksploatacji
          </label>
          /
          <label class="crossout">
            <input type="checkbox" v-model="form.not_allowed" /> Niedopuszczone do dalszej eksploatacji
          </label>
        </div>

        <label style="display: block; margin-top: 15px;">Uwagi / Usterki / Zalecenia</label>
        <v-textarea v-model="form.remarks" />

        <div class="signature-row" no-generate>
          <div class="signature-block" :ref="(el) => {if(el) {signatureWidth = el.offsetWidth}}">
            <p><strong>Wykonał:</strong></p>
            <SignaturePad v-model="signatureDataUrl" :width="signatureWidth"/>
          </div>
          <div class="signature-block">
            <p><strong>Odebrał:</strong></p>
            <SignaturePad v-model="receiverSignatureDataUrl" :width="signatureWidth" />
          </div>
        </div>

        <label style="display: block; margin-top: 15px;">Adres e-mail do wysyłki PDF:</label>
        <input v-model="email" type="email" placeholder="np. jan.kowalski@example.com" style="width: 100%; padding: 8px; margin-bottom: 10px;" />

        <v-btn @click="sendEmail" class="submitButton" no-generate>Wyślij</v-btn>
        <v-btn type="submit" class="submitButton" no-generate>Generuj PDF</v-btn>
      </form>

    </div>

    <div v-else-if="loading"><Loading/></div>
    <div v-else>Protokół nie znaleziony. Przekierowywanie...</div>
  </template>

  <script setup>
  import { ref, onMounted, inject } from 'vue'
  import { useRoute, useRouter } from 'vue-router'

  const route = useRoute()
  const router = useRouter()
  const api = inject('cmms_api')

  const id = route.params.id
  const protocol = ref(null)
  const loading = ref(true)
  const signatureDataUrl = ref(null)
  const receiverSignatureDataUrl = ref(null)
  let signatureWidth = ref(400)

  const form = ref({
    building: '',
    address: '',
    device: '',
    model: '',
    localization: '',
    survey_freq: 'Roczny',
    date: '',
    activities: [],
    operational: false,
    non_operational: false,
    allowed: false,
    not_allowed: false,
    remarks: ''
  })

  const email = ref('')

  const sendEmail = async () => {
    if (!email.value || !email.value.includes('@')) {
      alert('Wprowadź poprawny adres e-mail.');
      return;
    }

    try {
      await api.sendEmail(
        email.value,
        id,
        form.value,
        signatureDataUrl.value
      )
    } catch (error) {
      console.error(error);
      alert('Błąd podczas wysyłania e-maila.');
    }
  }


  onMounted(async () => {
    try {
      const res = await api.getProtocol(id)
      if (res?.data?.id) {
        protocol.value = res.data
        form.value.activities = protocol.value.fields.activities.map(() => ({
          choice: '',
          comment: ''
        }))
      } else {
        router.push('/protocols') // fallback route if protocol is not found
      }
    } catch (e) {
      console.error(e)
      router.push('/protocols') // fallback route in case of error
    } finally {
      loading.value = false
    }
  })

  const submitForm = () => {
    const elementToPrint = document.querySelector("form");

    const clone = elementToPrint.cloneNode(true);
    console.log(clone.querySelectorAll('[no-generate]'));
    clone.querySelectorAll('[no-generate]').forEach(item => item.parentNode.removeChild(item))

    let txtareas = clone.querySelectorAll('textarea');
    txtareas.forEach((a) => {
        let parent = a.parentElement;
        let div = document.createElement('div');
        div.innerText = a.value;
        parent.replaceChild(div, a);
    })

    let inputs = clone.querySelectorAll('input[type="text"]');
    inputs.forEach((input) => {
        let parent = input.parentElement;
        let div = document.createElement('div');
        div.innerText = input.value;
        parent.replaceChild(div, input);
    });

    let selects = clone.querySelectorAll('select');
    selects.forEach((select) => {
        let parent = select.parentElement;
        let div = document.createElement('div');
        div.innerText = select.options[select.selectedIndex].text;
        parent.replaceChild(div, select);
    });

    let dateInputs = clone.querySelectorAll('input[type="date"]');
    dateInputs.forEach((input) => {
        let parent = input.parentElement;
        let div = document.createElement('div');
        div.innerText = input.value;
        parent.replaceChild(div, input);
    });

    const printWindow = window.open('', '_blank', 'width=800,height=600');
    printWindow.document.write(`
        <html>
        <head>
            <title>Print Protocol</title>
            <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
            td, th { border: 1px solid #ccc; padding: 8px; }
            th { background-color: #f4f4f4; }
            </style>
        </head>
        <body>
            <h1>${protocol.value.name}</h1>
            <p><strong>Autor:</strong> ${protocol.value.author_name}</p>
        </body>
        </html>
    `);

    printWindow.document.body.appendChild(clone);
    let signDiv = document.createElement('div');
    signDiv.innerHTML = `
      <div style="margin-top: 50px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <p><strong>Wykonał:</strong></p>
            ${signatureDataUrl.value ? `<img src="${signatureDataUrl.value}" style="max-height: 100px; border: 1px solid #ccc;" />` : '<p>............................</p>'}
          </div>
          <div>
            <p><strong>Odebrał:</strong></p>
            ${receiverSignatureDataUrl.value ? `<img src="${receiverSignatureDataUrl.value}" style="max-height: 100px; border: 1px solid #ccc;" />` : '<p>............................</p>'}
          </div>
        </div>
      </div>
    `;
    printWindow.document.body.appendChild(signDiv);

    // Trigger the print dialog
    printWindow.document.close();
    printWindow.onload = () => printWindow.print();
  }
  </script>

  <style scoped>
  .protocol {
    margin-top: 15px;
    padding: 10px;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 1em;
    margin-top: 10px;
  }

  td, th {
    border: 1px solid #ccc;
    text-align: left;
    padding: 6px;
  }

  ol {
    counter-reset: list-counter;
  }

  ol li {
    list-style-type: decimal;
    counter-increment: list-counter;
  }

  ol li::before {
    content: counter(list-counter) ". ";
  }

  input[type="text"], input[type="date"], select {
    width: 100%;
    color: black;
    padding: 6px;
    box-sizing: border-box;
  }

  textarea, .comment-text {
    color: black;
    width: 100%;
    border: 1px solid #ccc;
    font-size: 14px;
    line-height: 1.5;
    padding: 6px;
    box-sizing: border-box;
  }

  .submitButton {
    background-color: var(--arslightblue);
    border: none;
    color: white;
    padding: 12px 24px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 10px;
    cursor: pointer;
    border-radius: 4px;
  }

  .submitButton:hover {
    background-color: var(--arsdeepblue);
  }

  .signature-row {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    width: 100%;
    margin-top: 20px;
  }

  .signature-block {
    flex: 0 0 48%;
    max-width: 48%;
  }

  .signature-block canvas {
    width: 100% !important;
    max-width: 100% !important;
    height: auto;
    border: 1px solid #866c6c;
  }

  /* Responsive styles */
  @media (max-width: 768px) {
    .signature-row {
      flex-direction: column;
      gap: 10px;
    }

    .signature-block {
      max-width: 100%;
      flex: 1 1 100%;
    }

    .submitButton {
      width: 100%;
    }

    table td, table th {
      font-size: 14px;
    }

    input[type="text"], input[type="date"], select, textarea {
      font-size: 16px;
    }
  }
</style>

