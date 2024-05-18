<template>
    <div class="banner">
        <h1 class="text">BuReClass</h1>
        <h2 class="text">Найдём любой материал!</h2>
        <div style="display: flex;">
          <RouterLink to="materials" class="button">Перейти к сопоставлению материала</RouterLink>
          <button @click="showModal" class="button" style="margin-left: 12px;">Актуализировать КСР</button>
        </div>
        <dialog id="modal" @click="closeModal">
          <form v-on:submit.prevent="sync">
            <input type="file" id="inputFile" v-on:change="changeFile" required/>
            <button class="button">Актуализировать</button>
          </form>
        </dialog>
    </div>
</template>

<script>
  import axios from "axios";

  export default
  {
    data() {
      return {
        actualizeForm: {
          file: ''
        },
      }
    },
    methods: {
      sync() {
        let formData = new FormData();
        formData.append('file', this.actualizeForm.file);
        new Promise((resolve, reject) => {
          axios.post("/api/actualize", formData, { headers: { 'Content-Type': 'multipart/form-data' }})
            .then(resp => {
                if (resp.data.status) {
                  alert("Данные актуализированы!");
                }
                resolve(resp);
              })
            .catch(error => {
              console.log(error.response.status);
              if (error.response.status == 422) {
                alert("ОШИБКА: Неправильный формат файла!");
              } else {
                alert("ОШИБКА: Не удалось прочитать файл!");
              }
              reject(error)
            });
        });
      },
      changeFile() {
        this.actualizeForm.file = event.target.files[0];
      },
      showModal() {
        modal.showModal();
      },
      closeModal(e) {
        const dialogDimensions = modal.getBoundingClientRect()
        if (
          e.clientX < dialogDimensions.left ||
          e.clientX > dialogDimensions.right ||
          e.clientY < dialogDimensions.top ||
          e.clientY > dialogDimensions.bottom
        ) {
          modal.close()
        }
        },
    }
  }
</script>

<style>
  dialog {
    top: 50%;
    left: 50%;
    translate: -50% -50%;
    border-radius: 4px;
    border: 2px solid var(--vt-c-green);
    padding: 20px;
  }
  dialog[open] {
    display: flex;
  }
  form {
    display: grid;
    row-gap: 48px;
    height: min-content;
    align-self: center;
  }
  .banner {
    margin: 250px 0;
    display: grid;
    align-content: center;
    justify-items: center;
  }
  h1 {
    font-size: 50px;
  }
  h2 {
    font-size: 30px;
    margin-bottom: 20px;
  }
  .button {
    background-color: var(--vt-c-green);
    color: white;
    padding: 12px 24px;
    border-radius: 4px;
    font-size: 18px;
  }
  .button:hover {
    background-color: #008c49;
  }
</style>
