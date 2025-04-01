<template>
  <div class="p-4">
    <h1 class="text-xl font-bold mb-4">Buscar Operadora</h1>
    <input
      v-model="termo"
      @input="buscar"
      type="text"
      placeholder="Digite nome, CNPJ ou parte do nome"
      class="border p-2 rounded w-full mb-4"
    />

    <div v-if="carregando">Carregando...</div>
    <div v-else-if="resultados.length === 0 && termo.length > 2">Nenhum resultado encontrado.</div>

    <ul>
      <li
        v-for="(operadora, index) in resultados"
        :key="index"
        class="mb-2 border rounded p-2"
      >
        <strong>{{ operadora.nome_fantasia }}</strong><br />
        CNPJ: {{ operadora.cnpj }}<br />
        Razão Social: {{ operadora.razao_social }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      termo: '',
      resultados: [],
      carregando: false,
      timeout: null
    }
  },
  methods: {
    buscar() {
      clearTimeout(this.timeout)
      if (this.termo.length < 3) {
        this.resultados = []
        return
      }
      this.timeout = setTimeout(async () => {
        this.carregando = true
        try {
          const response = await fetch(`http://localhost:5000/buscar-operadora?q=${encodeURIComponent(this.termo)}`)
          const data = await response.json()
          console.log('Resultado da API:', data)  // ⬅️ Adicione essa linha aqui
          this.resultados = data
        } catch (error) {
          console.error('Erro na busca:', error)
          this.resultados = []
        } finally {
          this.carregando = false
        }
      }, 400)
    }
  }
}




</script>

<style scoped>
input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 1px #3b82f6;
}
</style>
