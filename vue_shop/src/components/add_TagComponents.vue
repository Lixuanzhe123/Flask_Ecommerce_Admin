<template>
    <el-input
        v-if="inputVisible"
        ref="InputRef"
        v-model="inputValue"
        class="input-new-tag"
        size="small"
        @keyup.enter="handleInputConfirm"
        @blur="handleInputConfirm"
        />
        <el-button :icon="Plus" v-else clas="button-new-tag ml-1" size="small" @click="showInput" type="success">
        添加新属性
        </el-button>
</template>


<script setup>
    import { Plus } from '@element-plus/icons-vue'
    
    import { nextTick, ref } from 'vue'
    


    const inputValue = ref('')
    const inputVisible = ref(false)
    const InputRef = ref(null)
    const emit=defineEmits(['addTagEvent'])

    const props=defineProps({
        row:{
            type:Object,//传递数据的类型
            default:()=>Object//默认值
        }
    })
    const showInput = () => {
        inputVisible.value = true
        nextTick(() => {
            InputRef.value.input.focus()
        })
    }

    const handleInputConfirm = () => {
        //触发事件
        emit('addTagEvent',{"inputValue":inputValue.value,"row":props.row})
        inputVisible.value = false
        inputValue.value = ''
    }


</script>


<style scoped>
 .input-new-tag{
    width: 90px;
    margin-left: 25px;
 }
 .button-new-tag{
    margin-left: 25px;
 }

</style>