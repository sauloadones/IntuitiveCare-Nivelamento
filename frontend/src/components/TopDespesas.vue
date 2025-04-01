<template>
  <div class="p-4">
    <h2 class="text-xl font-semibold mb-4">Top 10 Despesas</h2>

    <button @click="buscarDespesas('trimestre')" class="mr-2 px-3 py-1 border rounded">
      Último Trimestre
    </button>
    <button @click="buscarDespesas('ano')" class="px-3 py-1 border rounded">
      Último Ano
    </button>

    <table v-if="despesas.length" class="mt-4 w-full border">
      <thead>
        <tr>
          <th class="border p-2">REG ANS</th>
          <th class="border p-2">Trimestre</th>
          <th class="border p-2">Total</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(linha, index) in despesas" :key="index">
          <td class="border p-2">{{ linha.REG_ANS || linha.reg_ans }}</td>
          <td class="border p-2">{{ linha.TRIMESTRE || '—' }}</td>
          <td class="border p-2">{{ parseFloat(linha.TOTAL || linha.total).toFixed(2) }}</td>
        </tr>
      </tbody>
    </table>

    <p v-else class="mt-4">Nenhum dado encontrado.</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      despesas: []
    }
  },
  methods: {
    async buscarDespesas(tipo) {
      const rota =
        tipo === 'ano'
          ? 'http://localhost:5000/top-despesas-ano'
          : 'http://localhost:5000/top-despesas-trimestre'
      try {
        const res = await fetch(rota)
        const data = await res.json()
        this.despesas = data
      } catch (e) {
        console.error('Erro ao buscar despesas:', e)
      }
    }
  }
}
</script>
