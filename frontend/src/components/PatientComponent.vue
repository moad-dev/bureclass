<script setup>
defineProps(['title', 'date', 'diagnosis', 'img', 'id'])
</script>

<template>
    <div class="card">
        <img :src="img" alt="photo">
        <div class="card-body">
            <div class="card-text">
                <p>Пациент: {{ title }}</p>
                <p>Результат анализа: <span>{{ diagnosis }}</span></p>
                <p class="float-left">{{ date }}</p>
            </div>
            <slot></slot>
        </div>
    </div>
</template>

<style scoped>
.card{
    display: grid;
    width: fit-content;
}
h1{
    justify-self: center;
}
img{
    margin: 10px 0;
    justify-self: center;
    height: 300px;
    width: auto;
}
.card-text{
    display: grid;
    margin: 5px 10px;
}
.float-left{
    justify-self: start;
    color: var(--vt-c-text-light-2);
    font-weight: 700;
}
span {
    font-weight: bold;
}
.card-body {
    display: flex;
    justify-content: space-between;
}
</style>