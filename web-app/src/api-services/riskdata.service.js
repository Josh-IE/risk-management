import Axios from 'axios'

const RESOURCE_NAME = '/risk_data'

export default {
  /**
   * get() returns an axios request promise object that retrieves risk data by form submit id.
   * @param {number} id  form submit id of the riskdata to be retrieved.
   * @return {Promise} GET request Promise object.
   */
  get (id) {
    return Axios.get(`${RESOURCE_NAME}/${id}/`)
  },

  /**
   * create() returns an axios request promise object that creates risk data.
   * @param {object} data  risk data json object.
   * @return {Promise} POST request Promise object.
   */
  create (data) {
    return Axios.post(`${RESOURCE_NAME}/`, data)
  }
}
