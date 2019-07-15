// Edit.vue
<template>
  <div>
    <RiskModelUI
      :riskModel="riskModel"
      :title="title"
      @submit="updateRiskModel()"
    />
    <FeedbackDialog
      :dialogObject="dialogObject"
      :riskModel="riskModel"
    />
  </div>
</template>
<script>
import RiskModelService from '@/api-services/riskmodel.service'
import Utils from '@/utils'
import RiskModelUI from './RiskModelUI'
import FeedbackDialog from './FeedbackDialog'

export default {
  name: 'RiskModelEdit',
  components: {
    RiskModelUI,
    FeedbackDialog
  },
  data () {
    return {
      riskModel: {},
      dialogObject: {
        'source': 'edit',
        'dialog': false,
        'submitSuccess': false,
        'dialogTitle': '',
        'data': '',
        'formErrors': {}
      },
      title: 'Configure Risk Model'
    }
  },
  mounted: function () {
    this.getRiskModel()
  },
  methods: {
    displaySuccessDialog: function (data) {
      this.dialogObject.dialog = true
      this.dialogObject.submitSuccess = true
      this.dialogObject.dialogTitle = 'Risk Model Successfully Updated'
      this.dialogObject.data = data
    },
    displayErrorDialog: function (error) {
      this.dialogObject.dialog = true
      this.dialogObject.submitSuccess = false
      this.dialogObject.dialogTitle = 'Form Submit: Error'
      this.dialogObject.formErrors = error
    },
    getRiskModel: function () {
      let id = this.$route.params.id
      this.$emit('loader', true)
      RiskModelService.get(id).then((response) => {
        console.log(response.data)
        this.riskModel = response.data
        this.$emit('loader', false)
        this.$emit('notifySuccess', true)
      }).catch((error) => {
        console.log(error.response.data)
        this.$emit('loader', false)
        this.$emit('notifySuccess', false)
      })
    },
    updateRiskModel: function () {
      let id = this.riskModel.id
      this.$emit('loader', true)
      console.log(this.riskModel)
      Utils.nullBlankFields(this.riskModel)
      RiskModelService.update(id, this.riskModel)
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
