/**
 * Daybreak — daily briefing email.
 *
 * Runs every 10 minutes (time-driven trigger). Checks GitHub for a new
 * edition of briefing/email.html and emails it once each morning. Stays
 * silent when there's nothing new. It never sends before SEND_AFTER_HOUR,
 * so it can't release yesterday's edition just after midnight — the morning
 * routine doesn't publish today's edition until ~5:20am your time. If no new
 * edition has arrived by 9am, it sends one (and only one) "something's wrong"
 * heads-up for the day.
 */
const GITHUB_USER = 'Johnmon3';
const REPO = 'daily-briefing';
const BRANCH = 'main';
const TO = 'aahanprakash123@gmail.com,prakash@asi-world.com';
const SEND_AFTER_HOUR = 6; // never email before this hour (your local time); today's edition is ready ~5:20am
const LATE_HOUR = 9; // warn once if nothing new by this hour (your local time)

function sendDaybreak() {
  const props = PropertiesService.getScriptProperties();
  const today = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd');

  // Already sent today's edition? Nothing to do.
  if (props.getProperty('lastSentDate') === today) return;

  // Too early — the morning routine hasn't published today's edition yet.
  // Without this guard, the first run after midnight would email yesterday's file.
  if (new Date().getHours() < SEND_AFTER_HOUR) return;

  const url = 'https://raw.githubusercontent.com/' + GITHUB_USER + '/' + REPO +
              '/' + BRANCH + '/briefing/email.html?cb=' + Date.now();
  const resp = UrlFetchApp.fetch(url, { muteHttpExceptions: true });

  if (resp.getResponseCode() !== 200) {
    warnIfLate(props, today, 'Could not fetch the briefing file (HTTP ' +
      resp.getResponseCode() + '). The morning robot may not have run.');
    return;
  }

  const html = resp.getContentText();
  const hash = Utilities.base64Encode(
    Utilities.computeDigest(Utilities.DigestAlgorithm.MD5, html));

  // Same file as the last one we emailed — no new edition yet.
  if (props.getProperty('lastSentHash') === hash) {
    warnIfLate(props, today, 'The briefing file has not been updated since ' +
      'yesterday. The morning robot may have failed.');
    return;
  }

  // Strip HTML comments first so notes in the file can never leak into the subject.
  const cleaned = html.replace(/<!--[\s\S]*?-->/g, '');
  const m = cleaned.match(/<title>([\s\S]*?)<\/title>/i);
  const subject = m ? m[1].trim() : 'Daybreak — your morning briefing';

  MailApp.sendEmail({ to: TO, subject: subject, htmlBody: html });
  props.setProperty('lastSentHash', hash);
  props.setProperty('lastSentDate', today);
}

// Sends at most one warning email per day, and only after LATE_HOUR.
function warnIfLate(props, today, reason) {
  if (new Date().getHours() < LATE_HOUR) return;
  if (props.getProperty('lastWarnDate') === today) return;
  MailApp.sendEmail(TO, 'Daybreak: no briefing this morning', reason +
    ' Ask Claude to check the "Daybreak morning briefing" routine.');
  props.setProperty('lastWarnDate', today);
}
