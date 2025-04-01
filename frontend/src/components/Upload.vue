<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-2">Upload CSV</h2>
    <input type="file" @change="handleFile" />
    <button @click="upload" class="bg-blue-500 text-white px-4 py-2 rounded ml-2">Enviar</button>
    <div v-if="message" class="mt-4">{{ message }}</div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      file: null,
      message: ''
    }
  },
  methods: {
    handleFile(e) {
      this.file = e.target.files[0]
    },
    async upload() {
      const form = new FormData()
      form.append('file', this.file)
      const res = await axios.post('http://localhost:5000/upload', form)
      this.message = res.data.message
    }
  }
}
</script>
