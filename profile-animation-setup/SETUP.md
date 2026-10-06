# Manual installation

1. Open https://github.com/yuvaraj-20/yuvaraj-20. Create this public repository if it does not exist. Its name must exactly match your GitHub username.
2. Extract this ZIP. Put the CONTENTS of profile-animation-setup at the repository root. Preserve .github/workflows/profile-city.yml, scripts/build_pixel_city.py and both assets. Do not upload the ZIP itself. If you already have a README, merge the two image lines rather than overwriting your existing biography.
3. The easiest reliable upload uses GitHub Desktop: clone the profile repository, copy the extracted files into its local folder, commit, and Push origin. Enable hidden files in your file manager if .github is not visible.
4. IMPORTANT: after copying the files, verify scripts/build_pixel_city.py AND scripts/render_profile_gifs.cjs appear on GitHub. The first installation omitted the scripts and workflow folders. Add the workflow explicitly using GitHub → Add file → Create new file, filename .github/workflows/profile-city.yml, and paste the included YAML. Then go to the repository's Actions tab, select Update Profile Animations, and click Run workflow on the default branch. A successful run replaces the demo city with actual GitHub calendar data, renders 80-frame looping GIFs for BOTH designs, and switches the README image links to GIF. The SVG references remain until rendering succeeds, so the existing images stay visible during setup.
5. Open assets/pixel-city.svg and then your profile. Confirm the demo label is gone and the contribution count looks reasonable. Refresh the page if GitHub's image cache still shows the previous asset.
6. Wait for Generate city from contributions, Render looping GIFs, and Commit updated animation to finish successfully. Check assets/craftele-comic.gif and assets/pixel-city.gif were committed and README points to them.
7. The scheduled refresh is 02:23 UTC / 07:53 IST daily. GitHub schedules can be delayed and inactive public repositories may have scheduled workflows disabled after 60 days. Rerun manually if needed.

## Private contribution counts

The workflow first uses the repository GITHUB_TOKEN and can read public activity. This may underrepresent Yuva's work in private Craftelé repositories. For private/internal contribution counts, GitHub documents the read:user scope on the contribution collection.

If required, create a classic personal access token with ONLY read:user, set an expiry, and add it as the repository Actions secret PROFILE_TOKEN (Settings → Secrets and variables → Actions → New repository secret). Do not add repo/write scopes just for this count-only query. Do not paste the token in README or code. The token retrieves dates and counts; the script does not query repository names or commit content. Adding private counts to a public profile is your choice. Revoke the token to remove that access.

If the API refuses access, keep the public-only result or review the token's account/organization restrictions. Do not increase permissions blindly.

## What these files do

- assets/craftele-comic.svg: the selected comic with looping steam, sparkles, screen light, yarn, and subtle hand/plant motion. MonoFit is removed. This is layered artwork; it is not generated character video. README SVGs have no clickable panel exploration.
- assets/pixel-city.svg: animated isometric city, one tile per calendar day, tower height based on GitHub contributionLevel. Crane, window lights, and vehicle are decorative.
- scripts/build_pixel_city.py: dependency-free Python generator using the GitHub GraphQL calendar, with no fallback to fake data if the API fails. An API failure leaves the existing asset intact and fails the workflow.
- .github/workflows/profile-city.yml: daily/manual refresh and a commit only when output changes. The built-in GitHub contribution graph is unchanged.

The generator, SVG XML, renderer syntax, and workflow YAML were locally validated. Browser installation in this environment failed, so the full GIF rendering step could not be tested here. The GitHub workflow must complete before this package can be considered verified on your profile. The authenticated workflow has not been run in your GitHub account. Image playback still depends on GitHub/browser animation and reduced-motion settings. If SVG animation is paused, open the image directly and check reduced-motion preferences.

## Troubleshooting

- Workflow not listed: check the workflow is on your default branch and the .github folder was uploaded.
- Push gets 403: the workflow requests contents:write, but repository/organization policy or branch protection may block automated pushes. Review the policy; do not disable protection blindly. A protected branch needs a PR-based update instead.
- GraphQL authentication error: renew PROFILE_TOKEN if you use it, or inspect the Actions API failure. Never print token values.
- City still says DEMO: the workflow has not completed successfully. Open its failed step.
- Comic is static: verify you uploaded the SVG instead of the screenshot. Reduced-motion mode intentionally stops movement.

## Official documentation

https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme
https://docs.github.com/en/graphql/reference/users
https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows

## V2 fix

The original repository upload had no scripts/build_pixel_city.py and no .github/workflows/profile-city.yml (both checked through the GitHub API). That prevents any live refresh. This version includes an explicit workflow-creation step plus a browser/ffmpeg GIF rendering job. Do not remove the DEMO label by editing text; run the actual-data generator.

The GIFs are generated by the workflow, not included as pre-rendered files in this ZIP. The source animations must be installed with all scripts. Do not upload only the README and assets.
