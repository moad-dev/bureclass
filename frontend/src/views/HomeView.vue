<template>
    <div class="banner">
        <h1 class="text">BuReClass</h1>
        <h2 class="text">Найдём любой материал!</h2>
        <RouterLink to="analyzes" class="button">Перейти к сопоставлению материала</RouterLink>
    </div>
</template>

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
