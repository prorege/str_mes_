import CustomStore from 'devextreme/data/custom_store';
import ApiService from '../utils/api-service';

export default class FindAddressStore extends CustomStore {
  constructor () {
    const apiService = new ApiService('/api/mes/v1/find-address');

    let options = {
      key: 'road',
      loadMode: 'processed',

      byKey (key) {
        console.log(key)
        return
      },

      // GET MANY
      load(options) {
        if (!this.keyword) {
          return new Promise((resolve) => {
            resolve({data: [], totalCount: 0})
          })
        }

        const { skip, take } = options;
        const params = {}
        params.keyword = this.keyword

        if (typeof skip === 'number' && typeof take === 'number') {
          params.results_per_page = take;
          params.page = Math.floor(skip / take) + 1;
        }

        return apiService
          .post('', params)
          .then(response => {
            return response.data
          })
          .catch((err) => {
            if (err.response) throw err.response.data
            else throw '정보 열람에 실패했습니다'
          });
      }
    };

    super(options);
    this.keyword = null
  }
}