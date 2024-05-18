<template>
    <label for="inputString">Введите название строительного материала</label>
    <input id="inputString" class="left-margin" v-model="object_name"/>
    <button @click="searchBRC" class="big-button">Сопоставить</button>
    <div>
        <table>
            <tr>
                <th>Код ресурса</th>
                <th>Наименование</th>
                <th>Единица измерения</th>
                <th>Точность сопоставления</th> 
            </tr>
        
            <td>{{ code }}</td>
            <td>{{ true_object_name }}</td>
            <td>{{ unit_of_measurement }}</td>
            <td>{{ score }}</td>
        </table>
    </div>
</template>

<script>
import axios from "axios";

export default
{
    data() {
        return {
            object_name: '',
            true_object_name: '',
            code: '',
            unit_of_measurement: '',
            score: '',
            msg: '',
        }
    },
    methods: {
        searchBRC() {
            axios.get("/api/search", {params: {object_name: this.object_name}})
                .then((res) => {
                    console.log(this.object_name);
                    this.code = res.data.code;
                    this.true_object_name = res.data.object_name;
                    this.unit_of_measurement = res.data.unit_of_measurement;
                    this.score = res.data.score;
            })
        },
    },
    computed:{
        
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
    .left-margin {
        margin-left: 20px;
    }
    .button-div {
        display: flex;
        justify-content: space-between;
    }
    .big-button {
        margin: 20px;
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