import Axios from 'axios'

const RESOURCE_NAME = '/risk_data_log'

export default {
  /**
   * getAll() returns an axios request promise object that retrieves a list of risk data submission events.
   * @param {number} id  risk model id.
   * @return {Promise} GET request Promise object.
   */
  getAll (id) {
    return Axios.get(`${RESOURCE_NAME}/?risk_model=${id}`)
  }
}
