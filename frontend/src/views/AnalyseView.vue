<template>
    <form v-on:submit.prevent="searchBRC">
        <div style="display: grid;">
            <div class="input-container">
                <label for="inputString">Введите название строительного ресурса</label>
                <input id="inputString" class="big-input" v-model="object_name" required />
            </div>
            
            <div class="input-container">
                <label for="inputLimit">Топ-N возможных вариантов</label>
                <input id="inputLimit" class="big-input" v-model="limit" type="number" min="1" required />
            </div>
            <input type="submit" class="big-button" value="Сопоставить"/>
        </div>        
    </form>
    <div v-if="objects.length != 0" class="table-container">
        <table>
            <tr>
                <th>Код ресурса</th>
                <th>Наименование</th>
                <th>Коэффициент пересчёта ед. изм.</th>
                <th>Точность сопоставления</th> 
            </tr>
            <tr v-for="object in objects">
                <td>{{ object.code }}</td>
                <td>{{ object.object_name }}</td>
                <td>{{ object.unit_of_measurement }}</td>
                <td>{{ object.score }}</td>
            </tr>
        </table>
    </div>
</template>

<script>
import axios from "axios";

export default
{
    data() {
        return {
            objects: [],
            limit: 1,
            object_name: '',
            code: '',
            unit_of_measurement: '',
            score: '',
            msg: '',
        }
    },
    methods: {
        searchBRC() {
            axios.get("/api/search", {params: {object_name: this.object_name, limit: this.limit}})
                .then((res) => {
                    console.log(res.data);
                    this.objects = res.data;
            })
        },
    },
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
    label {
        align-self: center;
    }
    .left-margin {
        margin-left: 20px;
    }
    @media (width <= 680px) {
        .table-container {
            width: 100vw;
            overflow-x: scroll;
            padding: 0px 12px;
        }
    }
    .button-div {
        display: flex;
        justify-content: space-between;
    }
    .input-container {
        display: flex;
        margin-top: 20px;
    }
    .big-input {
        margin-left: 20px;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 16px;
        flex-grow: 1;
    }
    .big-button {
        margin: 24px 0px;
        background-color: var(--vt-c-green);
        color: white;
        padding: 12px 20px;
        border-radius: 4px;
        font-size: 18px;
        flex-grow: 1;
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
    th:nth-child(1),
    td:nth-child(1) {
        width: min-content;
        white-space: nowrap;
    }
    th:nth-child(2),
    td:nth-child(2) {
        width: 70%;
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
