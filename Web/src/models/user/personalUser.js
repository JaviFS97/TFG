// Models
import User from './user'
import Vehicule from '../vehicule/vehicule'
import OrganizationUser from './organizationUser'

// Firebase
import {db} from '@/firebase'

/**
 * Represents a personal user.
 */
export default class personalUser extends User{

    /**
     * Basic constructor of personal user.
     * I added brackets in parameters for pass named parameters.
     * @param {String} email 
     * @param {String} password 
     * @param {String} nick 
     * @param {String} name 
     * @param {String} lastName 
     * @param {String} country 
     */
    constructor({email, password, nick, name, lastName, country}){
        super(email, password)
        this.nick = nick;
        this.name = name;
        this.lastName = lastName;
        this.country = country;
        this.uid = undefined
    }

    /**
     * Get uid of the loged user.
     */
    async getUID(){
        let usersNamesDoc = await db.collection('usersNames').doc(this.nick).get()
        this.uid = usersNamesDoc.data().uid
    }

    /**
     * Add a new personal user to Firebase database.
     * This methods add the information about user to 'users' and 'usersNames' collections. 
     * @param {Promise<UserCredential>} credentials of user.
     */
    async newPersonalUserInDatabase(credentials){
        // Obtain user id from credentials 
        this.uid = credentials.user.uid

        // Add new user to the two collections, for this reason I use batch.
        let batch = db.batch()

        batch.set(db.collection('users').doc(this.uid), {
                                                         nick: this.nick,
                                                         name: this.name,
                                                         lastName:  this.lastName,
                                                         country: this.country,
                                                        })
        batch.set(db.collection('usersNames').doc(this.nick), {
                                                                uid: this.uid
                                                              })

        await batch.commit()
    }

    /**
     * Get all the vehicules of the loged user.
     * @returns {Promise<>} 
     */
    async loadVehicules() {
        let vehicules = []
        if (!this.uid)
            await this.getUID()

        let vehiculesOnDatabase = await db.collection('users').doc(this.uid).collection('vehicules').get()
        vehiculesOnDatabase.forEach( vehicule => {      
            let loadVehicule = new Vehicule(vehicule.data().plate, 
                                        vehicule.data().name, 
                                        vehicule.data().type,
                                        vehicule.data().brand,
                                        vehicule.data().model,
                                        vehicule.data().height,
                                        vehicule.data().width,
                                        vehicule.data().depth)
            vehicules.push(loadVehicule)

            console.log(vehicule)
        })
        return vehicules
    }

    /**
     * Add a new vehicule to user's vehicules fleet .
     * @param {Vehicule} vehicule 
     */
    async saveVehicule(vehicule) {
        // Obtain user id from credentials 
        if (!this.uid)
            await this.getUID()        
        
        return await vehicule.createVehicule(this.uid)
    }

    async deleteVehicule(vehicule){
        // Obtain user id from credentials 
        if (!this.uid)
            await this.getUID()      

        return await vehicule.deleteVehicule(this.uid)

    }


    /**
     * listens to all the changes that hapen in the user's vehicules database.
     */
    async listenerVehicules() {
        // Obtain user id from credentials 
        if (!this.uid)
            await this.getUID()    
            
        let vehicules = []

        await db.collection('users').doc(this.uid).collection('vehicules').onSnapshot(querySnapshot => {
            querySnapshot.docChanges().forEach(change => {
            if (change.type === 'added' || change.type === 'modified') {
                //console.log('New/modified Vehicule: ', change.doc.data())
                let vehicule = change.doc.data()
                let loadVehicule = new Vehicule(vehicule.plate, 
                                                vehicule.name, 
                                                vehicule.type,
                                                vehicule.brand,
                                                vehicule.model,
                                                vehicule.height,
                                                vehicule.width,
                                                vehicule.depth)
                vehicules.push(loadVehicule)
            }
            if (change.type === 'removed') {
                //console.log('Removed Vehicule: ', change.doc.data())
            }
            })
        })    
        return vehicules
    }


    /**
     * For each organization in list, send a request to be a part of this organization.
     * @param {List} listOfOrganizations 
     */
    async requestInvitation(listOfOrganizations){
        // Obtain user id from credentials 
        if (!this.uid)
            await this.getUID()    

        for (const org of listOfOrganizations){
            let batch = db.batch()
            batch.set(db.collection('users').doc(this.uid).collection('organizations').doc(org.oid), { 'requestStatus': 'SENT', })
            batch.set(db.collection('organizations').doc(org.oid).collection('userRequest').doc(this.uid), { })
            await batch.commit()
        }
    }


    /**
     * Obtain all the organizations it belongs to.
     */
    async getOrganizations(){
        // Obtain user id from credentials 
        if (!this.uid)
            await this.getUID()    

        let organizations = []

        let organizationsDoc = await db.collection('users').doc(this.uid).collection('organizations').get()
        organizationsDoc.forEach( org => {      
            const organization = {}

            organization.oid = org.id
            organization.requestStatus = org.data().requestStatus
            organizations.push(organization)
        })

        return organizations
    }

    /**
     * Get all the parkings associated to an organization id.
     * @param {String} oid 
     */
    async getParkingsOfOrganization(oid){
        // Obtain user id from credentials 
        if (!this.uid)
            await this.getUID()    
            
        let parkings = []

        let parkingsDoc = await db.collection('users').doc(this.uid).collection('organizations').doc(oid).collection('parkings').get()
        parkingsDoc.forEach( park => {      
            const parking = {}

            parking.pid = park.id
            parking.title = park.data().title

            parkings.push(parking)
        })

        return parkings
    }


    async getPersonalUserByUID(uid){
        let organizationDoc = await db.collection('users').doc(uid).get()
        return organizationDoc.data()
    }


    /**
     * Rent out the car park
     * @param {String} pid: parking id
     * @param {Array[String]} dates
     * @param {String} startHour
     * @param {String} endHour     
     */
    async publishRent(pid, dates, startHour, endHour, coordenateLAT, coordenateLNG) {
        if (!this.uid)
            await this.getUID()  
                  
        let batch = db.batch()
        // batch.set(db.collection('users').doc(this.uid).collection('organizations').doc(org.oid).collection('parkings').doc(pid), { })
        batch.set(db.collection('rentGarajeSpace').doc(pid), { 'uidOwner': this.uid, 'dates': dates, 'startHour': startHour, 'endHour': endHour, 'coordenateLAT': coordenateLAT, 'coordenateLNG': coordenateLNG })
        await batch.commit()
    }

    async getRentList(){
        if (!this.uid)
            await this.getUID()     

        let rents = []
        let rentsDoc = await db.collection('users').doc(this.uid).collection('parkingsRent').get()
        rentsDoc.forEach( r => {      
            const rent = {}

            rent.uidOwner = r.data().uidOwner
            rent.pid = r.data().pid

            rents.push(rent)
        })

        return rents            
    }
}