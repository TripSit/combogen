export async function grabInteractionsGithub(url: string) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return await response.json();
  } catch (err) {
    throw err; // rethrow the error so it can be caught in the calling context
  }
}
