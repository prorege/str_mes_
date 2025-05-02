import { saveAs } from 'file-saver';

export async function downloadFile(url, fetchProps) {
  try {
    const response = await fetch(url, fetchProps);

    if (!response.ok) throw new Error(response)

    const filename = response.headers.get('content-disposition')
      .split(';')
      .find(n => n.includes('filename='))
      .replace('filename=', '')
      .trim()
    ;

    const blob = await response.blob();
    saveAs(blob, decodeURIComponent(filename));

  } catch (error) {
    throw new Error(error);
  }
}