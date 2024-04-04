const { CognitoIdentityProviderClient, InitiateAuthCommand } = require("@aws-sdk/client-cognito-identity-provider");

const REGION = "ap-northeast-1";
const clientId = "6p5a5cfu647vlh0va0qehhvvlq";
const refreshToken = "eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.SYKf_HIJSgHwTG-wFI8jPrzej5J7LpA-j0qp_yBYhnxfPwxZ1uJIThUtpszOyNy3DG9O7NfLl0wL7FxsqfWtz2YE1VcaucvBqT04B5S9OhospiMnP7WnOZhurhxnBJBElAdPioh6DxCUEyC6ZHCAN-AOzTa-l_fqQ1Eaa7WvrmebPpCZAe_YsWIcMGLK4oqGSjiJC41BV4ogb-dOAn7M2VfOILGDJ75SZH4tkA6HRPHnqDertvM3E7Ceua2BlQHX30D2VuwDUft4Qm8czgTAGZnzPjcgyEYwBnAJR9nB47n24Ehqdg-LmduzGg6gy__N6S2qY2VqHUOgexDhpVedKg.hUetLDqLPsVjyfKU.LiBC_Fs_eDkDVg7sUMfOGNUsVHa3yu96sG-3SUnmgR8U5FeeKoXik2X3NLCzOJ6VWL1CkcNDR8JbAzsYadzv9mVBNkr4o4c23NKfj2EFk5aOnDBbJli7bKHAqHbWMycCC8hqP8afT12swAjcjD4UasBan04D1x0TVirhk1giU-kgitI79UBhPhFbEfezXZSJqkyDXen3Jp6L3yKF1zCahfKd3rKHumB7mtiqOtEDpH2QcD7ypo9mdniEICX4h52Al2GLjyXdVKID-9lD3OHkQUs8-8qgF11WFCUmMtmlQJ62-2GK9TE6MLAJzLVRZ_iQSpd4VqMPsIuksTJQaDb4CpWORhbqF1Y0YaiwH0i1UBNfobNqCYacnB_vwLA5j16H4Ucp2l_85rLmxU_z87_Yr_V3t_KDcInIGtNxxpitb1HXiq5t2xtsNFUQzOZRWngfm5jWHgaf1tKvUATuOaUUod5VUTFSNThHU1gjC5cOmOe0JM15CfWNFtCR0IsuYqo7NcQ7E0VDjKvwMoFGDU_6bfFK6X6yTYrZJCLfbNlxm_9o8VNYAX0y6eYUbDaiDtvjYVpcP06Vz7froJs1Hpv-ilvsmrWqJt-NaZyHtpfPO6AW36ORSBpwmbju14NCuNZVlEJ_xBorD8CnIqhp1Gta4g5u8wskIImLYpn6hH7rf-3r99bMHeixzuJW-EIpZi-JosH5IpH6ViuTJdPtFET7vfiGqaCZiObKDudPQOF35TUAi2NZRcqdza2G_CxTLMxf4o8ALCgWndbx0Ya4eUZj4sBdGgp2QpPJ_4GhWEI30Yz5jkrB890z5RWU0Pznxpa6eoHa9u-_Q0SITRYSutub-nQI4zjbcZSOmSBJCt7KMouwAfuLgXGHrrPvn3okuYq9epxP8NG2nAadbxw_H98NNdhkriJG4diMz1Ow1MiKgjkDkqnwy8CieFBhGPKdnSJrO7BFmvzWqmVV7yHYTX37OoetKTnhDn82iYyUhs5u2DbhLPG-nFGakIJqMMT-_xZdc73l8AWKQ_SVATvqnaUPkNwyQY90l8RRtpfVu0GeX7JFVSn0RtEadS1PRmdtxLTOioDs45hszW5TnO59nBWvmYtUpbJJGppZ3NVf9O_FA8Ncp8Dm_6qf-XjegKOfPpbzKO9WrcpXJBjTsr7s4XWxwepgsLvKa7W_pVkISaY8L8GCHyAguQZ1aOQOxVUt4m9pjonLPGZ28jU_LN3WQcK_wwNmVGk1Qjq7t7OfAl5vqV3yQb6HT2_tidzQqEV8V3fRuF5V8QhKOOpEwNK79Lg3.ZnSmJ61LICnAUb7Tv0L0cg";

const client = new CognitoIdentityProviderClient({ region: REGION });

const command = new InitiateAuthCommand({
  AuthFlow: "REFRESH_TOKEN_AUTH",
  AuthParameters: {
    REFRESH_TOKEN: refreshToken,
  },
  ClientId: clientId,
});

const refreshAccessToken = async () => {
  try {
    const response = await client.send(command);
    console.log("accessToken:", response.AuthenticationResult.AccessToken);
    console.log("idToken:", response.AuthenticationResult.IdToken);
  } catch (error) {
    console.error(error);
  }
};

refreshAccessToken();