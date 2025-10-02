export async function fetchFundHistory(
  fundIdList: Array<string|number>,
  startDate: string,
  endDate: string,
) {
  try {
    const params = new URLSearchParams({
      fund_ids: fundIdList.join(','),
      start_date: startDate,
      end_date: endDate,
    })

    const response = await fetch(`http://localhost:9000/funds/history?${params}`)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    return data;
  } catch (err) {
    const error = err?.message
    console.error('Fetch error:', err)
  } finally {
  }
}
