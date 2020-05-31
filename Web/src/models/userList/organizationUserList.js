// Firebase
import {db} from '@/firebase'

export default class OrganizationUserList{

    constructor(){
    }

    /**
     * Return a list of organizations registered in the app.
     */
    async getOrganizationList() {

        let organizations = []

        let organizationsNamesDoc = await db.collection('organizationsNames').get()
        organizationsNamesDoc.forEach( org => {      

            const organization = {}
            organization.name = org.id
            organization.oid = org.data().oid
            //organization.userList = org.data().

            organizations.push(organization)
        })

        return organizations
    }
}