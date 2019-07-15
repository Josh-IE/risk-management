<template>
  <div>
    <p class="display-2">Risk Data</p>
    <v-data-table
      :headers="headers"
      :items="riskdata"
      class="elevation-1"
      disable-initial-sort="true"
      :pagination.sync="pagination"
    >
      <template #no-data>
        <v-alert
          :value="true"
          color="error"
          icon="warning"
        >
          Sorry, nothing to display here
        </v-alert>
      </template>
      <template #items="props">
        <td class="text-xs-left">{{ props.item.field_name }}</td>
        <td class="text-xs-left">
          <span v-if="props.item.field_type === 'file'">
            <a :href=props.item.value>{{ props.item.value }}</a>
          </span>
          <span v-else>{{ props.item.value }}</span>
        </td>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import RiskDataService from '@/api-services/riskdata.service'

export default {
  name: 'RiskData',
  data () {
    return {
      headers: [
        {
          text: 'Field Name',
          align: 'left',
          sortable: false,
          class: ['subheading', 'font-weight-bold']
        },
        { text: 'Data', sortable: false, class: ['subheading', 'font-weight-bold'] }
      ],
      riskdata: [],
      pagination: {
        rowsPerPage: 20
      }
    }
  },
  mounted: function () {
    this.getRiskData()
  },
  methods: {
    getRiskData: function () {
      this.$emit('loader', true)
      let id = this.$route.params.id
      RiskDataService.get(id)
        .then((response) => {
          this.riskdata = response.data
          this.$emit('loader', false)
          this.$emit('notifySuccess', true)
        })
        .catch((err) => {
          this.$emit('loader', false)
          this.$emit('notifySuccess', false)
          console.log(err)
        })
    }
  }
}
</script>
