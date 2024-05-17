<script setup>
import PatientComponent from "@/components/PatientComponent.vue";
</script>

<template>
    <button @click="openCreateModal" class="big-button">Создать анализ</button>
    <dialog id="createModal">
        <form type="multipart/form-data" class="form-container">
          <input type="text" name="patient_id" v-model="analysisForm.patient_id" class="input-element border-round cool-padding" placeholder="Идентификатор пациента">
          <input type="file" name="image" v-on:change="changeFile" class="input-element" alt="image-input">
          <div class="button-div input-element">
            <button formmethod="dialog" type="submit" style="background-color: var(--vt-c-text-red-light); color: white" class="cool-padding">Отмена</button>
            <button @click="onSubmit" class="cool-padding submit-button">Создать анализ</button>
          </div>
        </form>
    </dialog>
    <div>{{ msg }}</div>
    <div>
        <table>
            <tr>
                <th>№ п/п</th>
                <th @click="sort('prediction')" class="row">Результат анализа <button v-if="currentSort === 'prediction'" @click="changeSortDir">{{ currentSortDir === 'asc' ? '▼' : '▲'}}</button></th>
                <th @click="sort('date')" class="row">Дата <button v-if="currentSort === 'date'" @click="changeSortDir">{{ currentSortDir === 'asc' ? '▼' : '▲'}}</button></th>
                <th @click="sort('patient_id')" class="row">
                    Идентификатор пациента
                    <button v-if="currentSort === 'patient_id'" @click="changeSortDir" style="margin: 0 4px">
                        {{ currentSortDir === 'asc' ? '▼' : '▲'}}
                    </button>
                    <select @change="filterPatient($event)" v-on:click.prevent.stop>
                      <option selected>Все</option>
                      <option v-for="id in patientsIds"> {{ id }} </option>
                    </select>
                </th>
            </tr>
            <tr v-for="(patient, index) in sortedPatients" class="row" @click="getRow">
                <td>{{ index + 1 }}</td>
                <td>{{ patient.prediction }}</td>
                <td>{{ patient.date }}</td>
                <td>{{ patient.patient_id }}</td>
                <td style="display: none">{{ patient.image_bytes }}</td>
                <td style="display: none">{{ patient._id }}</td>
            </tr>
        </table>
    </div>
</template>

<script>
import axios from "axios";
import { store } from '@/store'

export default
{
    data() {
        return {
            patients: [],
            currentSort:'date',
            filteredPatients: [],
            currentSortDir:'asc',
            selectedPatient: ['', '', '', '', ''],
            analysisForm: {
                patient_id: '',
                image: '',
            },
            analysisId: '',
            msg: '',
        }
    },
    methods: {
        getAnalyzes() {
            axios.get("/api/analyzes", {headers: {Authorization: "Bearer " + localStorage.getItem('user-token')}})
                .then((res) => {
                    this.patients = res.data.data;
            })
        },
        deletePatient() {
            new Promise ((resolve, reject) => {
            axios.delete('/api/analyzes/' + this.selectedPatient[5], {headers: {Authorization: "Bearer " + localStorage.getItem('user-token')}})
                .then(resp => {
                    resolve(resp)
                })
                .catch((error) => {
                    this.msg = error.response.data.error;
                    reject(error)
                });
            }).then(() => {
                this.$router.push('/analyzes');
                this.getAnalyzes(); // TODO: WORST PRACTISES => REPLACE LATER
            })
        },
        sort:function(s) {
            this.currentSort = s;
        },
        changeSortDir:function() {
            this.currentSortDir = this.currentSortDir==='asc'?'desc':'asc';
        },
        getRow(event) {
            this.selectedPatient = [
                event.target.closest("tr").childNodes[0].innerText,
                event.target.closest("tr").childNodes[1].innerText,
                event.target.closest("tr").childNodes[2].innerText,
                event.target.closest("tr").childNodes[3].innerText,
                'data:image/png;base64, ' + event.target.closest("tr").childNodes[4].innerText,
                event.target.closest("tr").childNodes[5].innerText,
                ]
        },
        changeFile(event){
            this.analysisForm.image = event.target.files[0];
        },
        createAnalysis(analysis) {
            new Promise ((resolve, reject) => {
                axios.post("/api/analyzes/predict", analysis, {headers: {Authorization: "Bearer " + localStorage.getItem('user-token'),}})
                    .then(resp => {
                        this.analysisId = resp.data.data._id
                        store.result = { // redundant if use modal
                            image_bytes: resp.data.data.image_bytes,
                            patient_id: resp.data.data.patient_id,
                            prediction: resp.data.data.prediction,
                            date: resp.data.data.date
                        }
                        resolve(resp)
                    })
                    .catch((error) => {
                        this.msg = error.response.data.error;
                        reject(error)
                    });
            }).then(() => {
                this.$router.push('/analyzes');
                this.getAnalyzes(); // TODO: WORST PRACTISES => REPLACE LATER
            })
        },
        onSubmit(evt) {
            evt.preventDefault();

            let formData = new FormData()
            formData.append('patient_id', this.analysisForm.patient_id)
            formData.append('image', this.analysisForm.image)
            this.createAnalysis(formData);
            this.initForm();
        },
        filterPatient(event) {
            this.filteredPatients = this.patients.filter(patient => patient.patient_id === event.target.value);
        },
    },
    created() {
        this.getAnalyzes();
    },
    computed:{
        filteredPatients:function() {
          return this.filteredPatients
        },
        sortedPatients:function() {
            if (this.filteredPatients === undefined || this.filteredPatients.length == 0)
            {
                return this.patients.sort((a,b) => {
                  let modifier = 1;
                  if(this.currentSortDir === 'desc') modifier = -1;
                  if(a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
                  if(a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
                  return 0;
                });
            }
            else
            {
                return this.filteredPatients.sort((a,b) => {
                  let modifier = 1;
                  if(this.currentSortDir === 'desc') modifier = -1;
                  if(a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
                  if(a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
                  return 0;
                });
            }
        },
        patientsIds:function () {
            return [...new Set(this.patients.map(patient => patient.patient_id).sort())];
        }
    }
}
</script>

<style scoped>
    .form-container {
        display: grid;
    }
    dialog {
        top: 50%;
        left: 50%;
        translate: -50% -50%;
        border-radius: 4px;
        border: 2px solid var(--vt-c-green);
        padding: 20px;
    }
    .button-div {
        display: flex;
        justify-content: space-between;
    }
    .big-button {
        margin: 12px 0;
        background-color: var(--vt-c-green);
        color: white;
        padding: 12px 24px;
        border-radius: 4px;
        font-size: 18px;
    }
    .border-round {
        border-radius: 2px;
        border: 1px solid black;
    }
    input[type=file]::file-selector-button {
        padding: 6px 12px;
    }
    .cool-padding {
        padding: 6px 12px;
    }
    .delete-button {
        color: white;
        background-color: var(--vt-c-text-red-light);
    }
    table {
        width: 100%;
        border-spacing: 0;
        border: 1px solid var(--vt-c-divider-dark-1);
    }
    td, th {
        border: 1px solid var(--vt-c-divider-dark-1);
    }
    th, td {
        padding: 5px 10px;
        border-top-width: 0;
        border-left-width: 0;
    }
    td {
        text-align: center;
    }
    th:last-child,
    td:last-child {
        border-right-width: 0;
    }
    tr:last-child td {
        border-bottom-width: 0;
    }
    .row:hover {
        background-color: var(--vt-c-green-light);
        cursor: pointer;
    }
    .input-element {
        margin: 12px 0;
    }
    .big-button:hover {
      background-color: #008c49;
    }
</style>