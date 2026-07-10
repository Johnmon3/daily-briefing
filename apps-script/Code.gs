/**
 * Daybreak — daily briefing email nudge.
 *
 * Fetches the latest briefing/email.html from the daily-briefing GitHub repo
 * and mails it to you. Pair with a time-driven trigger (see README).
 *
 * One-time setup after creating the GitHub repo:
 *   1. Set GITHUB_USER below to your GitHub username.
 *   2. In script.google.com, paste this file, run sendDaybreak once to
 *      grant permissions, then add a daily trigger for sendDaybreak.
 */
const GITHUB_USER = 'Johnmon3';
const REPO = 'daily-briefing';
const BRANCH = 'main';
const TO = 'aahanprakash123@gmail.com';

function sendDaybreak() {
  const url = 'https://raw.githubusercontent.com/' + GITHUB_USER + '/' + REPO +
              '/' + BRANCH + '/briefing/email.html?cb=' + Date.now();
  const resp = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
  if (resp.getResponseCode() !== 200) {
    MailApp.sendEmail(TO, 'Daybreak: briefing fetch failed',
      'Could not fetch ' + url + ' (HTTP ' + resp.getResponseCode() + '). ' +
      'The morning routine may not have run or pushed yet.');
    return;
  }
  const html = resp.getContentText();

  // Subject comes from the <title> tag the routine writes each morning.
  const m = html.match(/<title>([\s\S]*?)<\/title>/i);
  const subject = m ? m[1].trim() : 'Daybreak — your morning briefing';

  // Skip re-sending if today's file hasn't changed since yesterday's send.
  const props = PropertiesService.getScriptProperties();
  const hash = Utilities.base64Encode(
    Utilities.computeDigest(Utilities.DigestAlgorithm.MD5, html));
  if (props.getProperty('lastSentHash') === hash) {
    MailApp.sendEmail(TO, 'Daybreak: briefing is stale',
      'Today\'s email.html is identical to the last one sent — the morning ' +
      'routine may have failed. Check your scheduled agent.');
    return;
  }

  MailApp.sendEmail({ to: TO, subject: subject, htmlBody: html });
  props.setProperty('lastSentHash', hash);
}
