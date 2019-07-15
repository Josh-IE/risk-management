<template>
  <div>
    <p class="display-2">Risk Data Submissions</p>
    <v-data-table
      :headers="headers"
      :items="riskdatalog"
      class="elevation-1"
      disable-initial-sort=true
    >
      <template #no-data>
        <v-alert
          :value=true
          color="error"
          icon="warning"
        >
          Sorry, nothing to display here
        </v-alert>
      </template>
      <template #items="props">
        <td class="text-xs-left">{{ props.item.id }}</td>
        <td class="text-xs-left">{{ props.item.created_on }}</td>
        <td class="text-xs-left">
          <v-btn
            color="primary"
            dark
            class="mb-2"
            @click="loadRiskData(props.item.id)"
          >
            <v-icon
              small
              class="mr-2"
            >
              visibility
            </v-icon> View Data
          </v-btn>
        </td>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import RiskDataLogService from '@/api-services/riskdatalog.service'

export default {
  name: 'RiskDataLog',
  data () {
    return {
      headers: [
        {
          text: '# ID',
          align: 'left',
          sortable: true,
          class: ['subheading', 'font-weight-bold'],
          value: 'id'
        },
        { text: 'Time Submitted', value: 'created_on', class: ['subheading', 'font-weight-bold'] },
        { text: 'Action', sortable: false, align: 'left', class: ['subheading', 'font-weight-bold'] }
      ],
      riskdatalog: []
    }
  },
  mounted: function () {
    this.getRiskDataLog()
  },
  methods: {
    getRiskDataLog: function () {
      this.$emit('loader', true)
      let id = this.$route.params.id
      RiskDataLogService.getAll(id)
        .then((response) => {
          this.riskdatalog = response.data
          this.$emit('loader', false)
          this.$emit('notifySuccess', true)
        })
        .catch((error) => {
          this.$emit('loader', false)
          this.$emit('notifySuccess', false)
          console.log(error.response.data)
        })
    },
    loadRiskData: function (id) {
      this.$router.push({ name: 'risk-data', params: { id: id } })
    }
  }
}
</script>
