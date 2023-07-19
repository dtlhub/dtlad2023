migrate((db) => {
  const snapshot = [
    {
      "id": "5b62gswbvx6alk6",
      "created": "2023-07-10 06:39:35.697Z",
      "updated": "2023-07-17 14:05:09.813Z",
      "name": "workspaces",
      "type": "base",
      "system": false,
      "schema": [
        {
          "system": false,
          "id": "vwxx12eu",
          "name": "name",
          "type": "text",
          "required": true,
          "unique": false,
          "options": {
            "min": null,
            "max": null,
            "pattern": ""
          }
        },
        {
          "system": false,
          "id": "flunqi9k",
          "name": "owner",
          "type": "relation",
          "required": true,
          "unique": false,
          "options": {
            "collectionId": "_pb_users_auth_",
            "cascadeDelete": false,
            "minSelect": null,
            "maxSelect": 1,
            "displayFields": []
          }
        },
        {
          "system": false,
          "id": "gu5orpnc",
          "name": "description",
          "type": "text",
          "required": false,
          "unique": false,
          "options": {
            "min": null,
            "max": null,
            "pattern": ""
          }
        }
      ],
      "indexes": [
        "CREATE UNIQUE INDEX `idx_RpTwAg7` ON `workspaces` (\n  `name`,\n  `owner`\n)"
      ],
      "listRule": "@request.auth.id != ''",
      "viewRule": "@request.auth.id != ''",
      "createRule": "@request.auth.id != ''",
      "updateRule": null,
      "deleteRule": "@request.auth.id != ''",
      "options": {}
    },
    {
      "id": "_pb_users_auth_",
      "created": "2023-07-14 09:55:46.665Z",
      "updated": "2023-07-14 09:55:46.674Z",
      "name": "users",
      "type": "auth",
      "system": false,
      "schema": [],
      "indexes": [],
      "listRule": "id = @request.auth.id",
      "viewRule": "id = @request.auth.id",
      "createRule": "",
      "updateRule": "id = @request.auth.id",
      "deleteRule": "id = @request.auth.id",
      "options": {
        "allowEmailAuth": true,
        "allowOAuth2Auth": false,
        "allowUsernameAuth": true,
        "exceptEmailDomains": null,
        "manageRule": null,
        "minPasswordLength": 5,
        "onlyEmailDomains": null,
        "requireEmail": false
      }
    }
  ];

  const collections = snapshot.map((item) => new Collection(item));

  return Dao(db).importCollections(collections, true, null);
}, (db) => {
  return null;
})
