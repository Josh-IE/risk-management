// Create.vue
<template>
  <div>
    <RiskModelUI
      :riskModel="riskModel"
      :title="title"
      @submit="createRiskModel()"
    />
    <FeedbackDialog
      :dialogObject="dialogObject"
      :riskModel="riskModel"
    />
  </div>
</template>
<script>
import RiskModelService from '@/api-services/riskmodel.service'
import RiskModelUI from './RiskModelUI'
import FeedbackDialog from './FeedbackDialog'
import Utils from '@/utils'

export default {
  name: 'RiskModelCreate',
  components: {
    RiskModelUI,
    FeedbackDialog
  },
  data () {
    return {
      riskModel: {
        'name': null,
        'button': null,
        'description': null,
        'success_msg': null,
        'activated': true,
        'fields': []
      },
      dialogObject: {
        'source': 'create',
        'dialog': false,
        'submitSuccess': false,
        'dialogTitle': '',
        'data': '',
        'formErrors': {}
      },
      title: 'Create Risk Model'
    }
  },
  mounted: function () {
    this.getFieldTypeChoices()
  },
  methods: {
    displaySuccessDialog: function (data) {
      this.dialogObject.dialog = true
      this.dialogObject.submitSuccess = true
      this.dialogObject.dialogTitle = 'Risk Model Successfully Created'
      this.dialogObject.data = data
    },
    displayErrorDialog: function (error) {
      this.dialogObject.submitSuccess = false
      this.dialogObject.dialog = true
      this.dialogObject.dialogTitle = 'Form Submit: Error'
      this.dialogObject.formErrors = error
    },
    getFieldTypeChoices: function () {
      RiskModelService.getFieldTypes().then((response) => {
        console.log(response.data)
        this.field_type_choices = response.data
        this.$emit('loader', false)
        this.$emit('notifySuccess', true)
      }).catch((error) => {
        console.log(error.response.data)
        this.$emit('loader', false)
        this.$emit('notifySuccess', false)
      })
    },
    createRiskModel: function () {
      this.$emit('loader', true)
      Utils.nullBlankFields(this.riskModel)
      RiskModelService.create(this.riskModel)
        .then(response => {
          console.log(response.data)
          this.riskModel = response.data
          this.$emit('loader', false)
          this.$emit('notifySuccess', true)
          this.displaySuccessDialog(response.data)
        })
        .catch(error => {
          this.$emit('loader', false)
          this.$emit('notifySuccess', false)
          this.displayErrorDialog(error.response.data)
          console.log(error.response.data)
        })
    }
  }
}
</script>
