<template>
  <Upload />
  <TopDespesas />
  <BuscarOperadora />
</template>

<script>
import Upload from './components/Upload.vue'
import TopDespesas from './components/TopDespesas.vue'
import BuscarOperadora  from './components/BuscarOperadora.vue'

export default {
  components: {
    Upload,
    TopDespesas,
    BuscarOperadora
  }
}
</script>