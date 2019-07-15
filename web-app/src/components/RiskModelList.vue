// List.vue
<template>
  <div>
    <p class="display-2">List of Risk Models</p>
    <v-toolbar
      flat
      color="white"
    >
      <v-spacer></v-spacer>
      <v-btn
        color="primary"
        dark
        @click="createRiskModel"
      >
        <v-icon>add</v-icon> New Model
      </v-btn>
    </v-toolbar>
    <v-data-table
      :headers="headers"
      :items="riskModels"
      class="elevation-1"
      disable-initial-sort=true
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
        <td class="text-xs-left">{{ props.item.id }}</td>
        <td class="text-xs-left">{{ props.item.name }}</td>
        <td class="text-xs-left">
          <v-btn
            v-if="props.item.activated"
            color="info"
          >Active</v-btn>
          <v-btn
            v-else
            color="error"
          >InActive</v-btn>
        </td>
        <td class="text-xs-left">
          <v-btn
            color="primary"
            dark
            class="mb-2"
            @click="editRiskModel(props.item.id)"
          >
            <v-icon
              small
              class="mr-2"
            >
              build
            </v-icon> Edit Model
          </v-btn>

          <v-btn
            color="primary"
            dark
            class="mb-2"
            @click="loadRiskForm(props.item.id)"
          >
            <v-icon
              small
              class="mr-2"
            >
              visibility
            </v-icon> Load Form
          </v-btn>
          <v-btn
            color="primary"
            dark
            class="mb-2"
            @click="riskFormLogs(props.item.id)"
          >
            <v-icon
              small
              class="mr-2"
            >
              save
            </v-icon> Submissions
          </v-btn>
        </td>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import RiskModelService from '@/api-services/riskmodel.service'

export default {
  name: 'RiskModelList',
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
        { text: 'Name', value: 'name', class: ['subheading', 'font-weight-bold'] },
        { text: 'State', value: 'activated', class: ['subheading', 'font-weight-bold'] },
        { text: 'Actions', sortable: false, align: 'left', class: ['subheading', 'font-weight-bold'] }
      ],
      riskModels: []
    }
  },
  mounted: function () {
    this.getRiskModels()
  },
  methods: {
    getRiskModels: function () {
      this.$emit('loader', true)
      RiskModelService.getAll()
        .then((response) => {
          this.riskModels = response.data
          this.$emit('loader', false)
          this.$emit('notifySuccess', true)
        })
        .catch((error) => {
          this.$emit('loader', false)
          this.$emit('notifySuccess', false)
          console.log(error.response.data)
        })
    },
    editRiskModel: function (id) {
      this.$router.push({ name: 'risk-model-edit', params: { id: id } })
    },
    loadRiskForm: function (id) {
      this.$router.push({ name: 'risk-form', params: { id: id } })
    },
    riskFormLogs: function (id) {
      this.$router.push({ name: 'risk-form-log', params: { id: id } })
    },
    createRiskModel: function () {
      this.$router.push({ name: 'risk-model-create' })
    }
  }
}
</script>
