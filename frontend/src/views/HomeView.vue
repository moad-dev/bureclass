<script setup>
    import PopupComponent from "../components/PopupComponent.vue";
</script>

<template>
    <div class="banner">
        <h1 class="text">BuReClass</h1>
        <h2 class="text">Найдём любой материал!</h2>
        <div style="display: flex;">
          <RouterLink to="materials" class="button">Перейти к сопоставлению материала</RouterLink>
          <button @click="showModal" class="button" style="margin-left: 12px;">Актуализировать КСР</button>
        </div>
        <dialog id="modal" @click="closeModal">
          <form v-on:submit.prevent="sync" class="main-form">
            <input type="file" id="inputFile" v-on:change="changeFile" required/>
            <div>
                <label for="inputPassword">Пароль</label>
                <input type="password" id="inputPassword" v-model="password" required>
            </div>
            <button class="button">Актуализировать</button>
          </form>
        </dialog>
    </div>
    <Transition>
        <PopupComponent :success="this.popup.success" :title="this.popup.title" :show="this.popup.show" :text="this.popup.text">
        </PopupComponent>
    </Transition>
</template>

<script>
  import axios from "axios";

  export default
  {
    data() {
      return {
        actualizeForm: {
          file: '',
        },
        password: '',
        popup: {
            title: '',
            text: '',
            success: true,
            show: false,
        },
      }
    },
    methods: {
      sync() {
        let formData = new FormData();
        formData.append('file', this.actualizeForm.file);
        formData.append('password', this.password);
        new Promise((resolve, reject) => {
                  axios.post("/api/actualize", formData, { headers: { 'Content-Type': 'multipart/form-data' }})
            .then(resp => {
              // this.showPopup("failed", "ВНИМАНИЕ", "Файл обрабатывается, пожалуйста, подождите")
              setTimeout(function checker (callback) {
                axios.get("/api/actualize").then(function (response) {
                  if (response.data.status == "running") {
                    setTimeout(checker, 1000, callback);
                  }
                  if (response.data.status == "completed") {
                    callback("completed", "УСПЕХ", "Данные актуализированы");
                  }
                  if (response.data.status == "failed") {
                    callback("failed", "ОШИБКА", "Актуализация данных не была проведена");
                  }
                });
              }, 1000, this.showPopup);
              modal.close();
              resolve(resp);
            })
            .catch(error => {
              console.log(error.response.status);
              if (error.response.status == 400) {
                this.showPopup("failed", "ОШИБКА", "Неправильный формат файла");
              } else if (error.response.status == 423) {
                this.showPopup("failed", "ОШИБКА", "Файл ещё в обработке");
              } else if (error.response.status == 403) {
                this.showPopup("failed", "ОШИБКА", "Неправильный пароль");
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
      showPopup(status, title, text) {
        this.popup.title = title;
        this.popup.text = text;
        this.popup.success = status == "completed";
        this.popup.show = true;
        setTimeout(() => {this.popup.show = false}, 4000);
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
    .main-form {
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
    .v-enter-active,
    .v-leave-active {
    transition: opacity 0.5s ease;
    }
    .v-enter-from,
    .v-leave-to {
    opacity: 0;
    }
</style>
