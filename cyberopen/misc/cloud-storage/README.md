# Cloud Storage

Have you heard about this "cloud" thing that everyone is using? I think we can save a bunch of money by putting our cat photos there!

I have provided a service account key that you can use to authenticate and check that you can access the photos.

That service account shouldn't have access to anything other than the cat pictures, but this whole "eye aye em" thing is a bit confusing, so I'm not entirely sure!

We can't afford to have another data breach, so we need to be confident that our flags are secure before we make the switch.

## Challenge

For this challenge you were given a `lateral-replica.json` key to access the google cloud. The catch was that you were a `user-service-account` and the flag was only accessible to an `admin-service-account`.

I believe the challenge has been taken down so I cannot exactly show the step by step to getting the flag, but I know a lot of people were able to get to the point where they knew where the flag file was but couldn't read it due to permissions.

After doing a bit of looking around during the competition I came across this:

```
gcloud storage buckets list --impersonate-service-account=SERVICE_ACCT_EMAIL
```

The gcloud cli has a flag that allows you to impersonate a service account. I read a bit about it [here](https://cloud.google.com/docs/authentication/use-service-account-impersonation) and tried it out on this challenge. I impersonated the admin account using the email `admin-service-account@lateral-replica-423406-n3.iam.gserviceaccount.com`.

Here's an example of it executing a privileged command after I had set the impersonation flag:
```
└─$ gcloud projects list
WARNING: This command is using service account impersonation. All API calls will be executed as [admin-service-account@lateral-replica-423406-n3.iam.gserviceaccount.com].
```


## Flag

`SIVBGR{7h3_51nc3r357_f0rm_0f_fl4773ry}`
