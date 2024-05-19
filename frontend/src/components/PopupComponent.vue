<template>
    <div v-if="show" class="popup">
        <img v-if="success" src="../assets/green-check.png" alt="logo">
        <img v-if="!success" src="../assets/red-cross.png" alt="logo">
        <div class="popup-text">
            <h1>{{ title }}</h1>
            <div class="text">
                {{ text }}
            </div>
        </div>
    </div>
</template>

<script>
    export default
    {
        props: {
            title: {
                type: String,
                default: 'Title'
            },
            success: {
                type: Boolean,
                default: true
            },
            show: {
                type: Boolean,
                default: false
            },
            text: {
                type: String,
                default: 'Text'
            }
        },
    }
</script>

<style scoped>
    .popup {
        display: flex;
        position: fixed;
        bottom: 12px;
        right: 12px;
        border: 2px solid var(--vt-c-green);
        border-radius: 2px;
    }
    .popup-text {
        display: grid;
        margin: 6px 6px;
    }
    img {
        width: 48px;
        height: 60px;
        align-self: center;
        margin: 0px 6px;
    }
    h1
    {
        text-align: left;
        font-size: larger;
        color: var(--vt-c-black-soft);
        border-bottom: 1px solid var(--vt-c-divider-light-2);
    }
    .text {
        min-height: 48px; 
        min-width: 200px;
        text-align: start;
    }
</style>