import ApiService from "../utils/api-service"

const findBusinessNumberApi = new ApiService('/api/mes/v1/find-business-number')

/**
 * @param {String} busnNum 
 * @returns 
 *  b_stt : 01: 계속사업자, 02: 휴업자, 03: 폐업자
 *  b_stt_cd : 01: 계속사업자, 02: 휴업자, 03: 폐업자
 *  end_dt : 폐업일 (YYYYMMDD 포맷)
 */
const findBusinessNumber = async (busnNum) => {
  if (!busnNum) throw Error('1 argument required')
  const {data} = await findBusinessNumberApi.get(busnNum)
  return data
}

export {findBusinessNumberApi, findBusinessNumber}
export default findBusinessNumber