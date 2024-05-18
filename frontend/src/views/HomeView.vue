<template>
    <div class="banner">
        <h1 class="text">BuReClass</h1>
        <h2 class="text">Найдём любой материал!</h2>
        <div style="display: flex;">
          <RouterLink to="materials" class="button">Перейти к сопоставлению материала</RouterLink>
          <button @click="sync" class="button" style="margin-left: 12px;">Актуализировать КСР</button>
        </div>
    </div>
</template>

<script>
  import axios from "axios";

  export default
  {
      methods: {
          sync() {
              axios.get("/api/actualize")
                  .then((res) => {
                      if (res.data.status) {
                        alert("Синхронизация прошла успешно!");
                      } else {
                        alert("ОШИБКА: Синхронизация не произошла!");
                      }
              })
          },
      },
  }
</script>

<style>
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
