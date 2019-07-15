import Vue from 'vue'
import Router from 'vue-router'

import RiskModelList from '@/components/RiskModelList.vue'
import RiskModelCreate from '@/components/RiskModelCreate.vue'
import RiskModelEdit from '@/components/RiskModelEdit.vue'
import RiskForm from '@/components/RiskForm.vue'
import RiskFormLog from '@/components/RiskFormLog.vue'
import RiskData from '@/components/RiskData.vue'

Vue.use(Router)

export default new Router({
  routes: [{
    path: '/',
    name: 'risk-model-list',
    component: RiskModelList
  },
  {
    path: '/risk/create',
    name: 'risk-model-create',
    component: RiskModelCreate
  },
  {
    path: '/risk/edit/:id',
    name: 'risk-model-edit',
    component: RiskModelEdit
  },
  {
    path: '/risk/form/:id',
    name: 'risk-form',
    component: RiskForm
  },
  {
    path: '/risk/log/:id',
    name: 'risk-form-log',
    component: RiskFormLog
  }, {
    path: '/risk/data/:id',
    name: 'risk-data',
    component: RiskData
  }
  ]
})
